import eel
from AudioTrack import AudioTrack
from Album import Album
from pathlib import Path
from pygame import mixer
from jinja2 import Environment, FileSystemLoader
import sqlite3
from sqlite3 import Error
import collections
from Player import Player


paused = False

#Jinja
file_loader = FileSystemLoader('web/templates')
env = Environment(loader=file_loader)


home = Path.home()
music_dir = home / "music/"
print ("music dir:", music_dir)
#song_paths = music_dir.rglob("*.mp3")


player = Player()


def load():
    tracks = []
    artists = set()
    albums = set()
    conn = sqlite3.connect('MusicLibrary.db')
    c = conn.cursor() 
    query = ("""SELECT track_name, path, album, artist, id FROM tracks order by id asc limit 250;""")
    c.execute(query)
    queryResults = c.fetchall()
    for row in queryResults:
        print(row)     
        file_path = row[1].replace("\\", "\\\\")
        name = row[0]
        album = row[2]
        artist = row[3]
        id = row[4]
        track = AudioTrack(id=id, name=name, album=album, artist=artist, file_path=file_path)
        tracks.append(track)
        ustr = ".thumbnail"
        album = Album(name=album, artist=artist, img=album + ustr)
        albums.add(album)
        artists.add(artist)
    c.close()
    template = env.get_template('index.html')
    output = template.render(tracks=tracks, albums=albums, artists=artists)
    data_folder = Path(__file__).parent
    rendered_filename = data_folder / 'web' / 'templates' / 'main.html'
    with open(rendered_filename, "w", encoding='utf-8') as f:
        f.write(output)
    


load()
eel.init('web')


@eel.expose
def reload():
    load()


@eel.expose
def get_artist_view(artistName):
    conn = sqlite3.connect('MusicLibrary.db')
    c = conn.cursor() 
    print('getting artist data')
    tracks = []
    artists = set()
    albums = set()
    query = ("""SELECT track_name, path, album, artist, id FROM tracks where artist=? order by id asc""")
    c.execute(query, (artistName,))
    queryResults = c.fetchall()
    for row in queryResults:
        print(row)     
        track = AudioTrack(id=row[4], name=row[0], album=row[2], artist=row[3], file_path=row[1].replace("\\", "\\\\"))
        tracks.append(track)
        album = Album(name=row[2], artist=row[3], img=row[2] + ".thumbnail")
        albums.add(album)
        artists.add(row[3])
    c.close()
    template = env.get_template('index.html')
    output = template.render(tracks=tracks, albums=albums, artists=artists)
    data_folder = Path(__file__).parent
    rendered_filename = data_folder / 'web' / 'templates' / 'main.html'
    with open(rendered_filename, "w", encoding='utf-8') as f:
        f.write(output)



#Metadata retrieval from music library
@eel.expose
def get_song(id):
    conn = sqlite3.connect('MusicLibrary.db')
    c = conn.cursor()
    query = ("""SELECT track_name, artist, album, path from tracks where id=?""")
    c.execute(query,(id,))
    queryResults = c.fetchall()
    for row in queryResults:
        song = row[0]
        album = row[2]
        path = row[3]
    player.update(id, row[0], row[1])
    player.display()
    c.close()
    return [song, album, path]



@eel.expose
def get_next_song(id):
    conn = sqlite3.connect('MusicLibrary.db')
    c = conn.cursor()
    query = ("""select path, id from tracks where id = (select min(id) from tracks where id > ?)""")
    c.execute(query, (id,))
    queryResults = c.fetchall()
    for row in queryResults:
        print(row)
        next_track = row[0]
        next_id = row[1]
    c.close()
    return [next_track, next_id]


@eel.expose
def get_previous_song(id):
    conn = sqlite3.connect('MusicLibrary.db')
    c = conn.cursor()
    query =("""select path, id from tracks where id = (select max(id) from tracks where id < ?)""")
    c.execute(query, (id,))
    queryResults = c.fetchall()
    for row in queryResults:
        print(row)
        previous_track = row[0]
        previous_id = row[1]
    c.close()
    return [previous_track, previous_id]



#Music Player functionalities
@eel.expose
def play_song(song):
    # Starting the mixer 
    mixer.init() 
    
    # Loading the song 
    print("Loading..", song)
    mixer.music.load(song)
    
    # Setting the volume 
    mixer.music.set_volume(0.7) 
    
    # Start playing the song 
    mixer.music.play() 


@eel.expose
def stop_song():
    mixer.music.stop()
    mixer.music.unload()


@eel.expose
def pause_song():
    global paused
    paused = True
    print("pausing song..")
    mixer.music.pause()
    
@eel.expose
def unpause_song():
    global paused
    paused = False
    print("resuming song..")
    mixer.music.unpause()


    
eel.start('templates/main.html',port=0, size=(800, 600))

