import eel
from AudioTrack import AudioTrack
from Album import Album
from pathlib import Path
from pygame import mixer
from jinja2 import Environment, FileSystemLoader
import sqlite3
from sqlite3 import Error
import collections


conn = sqlite3.connect('MusicLibrary.db')
c = conn.cursor() 

paused = False

#Jinja template
file_loader = FileSystemLoader('web/templates')
env = Environment(loader=file_loader)
template = env.get_template('index.html')


home = Path.home()
music_dir = home / "music/"
print ("music dir:", music_dir)
song_paths = music_dir.rglob("*.mp3")

tracks = []
artists = set()
albums = set()


#SQLite query, results parsing
query = ("""SELECT track_name, path, album, artist, id FROM tracks order by id asc limit 50;""")
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

output = template.render(tracks=tracks, albums=albums, artists=artists)
data_folder = Path(__file__).parent
rendered_filename = data_folder / 'web' / 'templates' / 'main.html'
with open(rendered_filename, "w", encoding='utf-8') as f:
    f.write(output)


eel.init('web')



#Metadata retrieval from music library
@eel.expose
def get_album(id):
    conn = sqlite3.connect('MusicLibrary.db')
    c = conn.cursor() 
    query = ("""SELECT album from tracks where id = ?""")
    c.execute(query, (id,))
    queryResults = c.fetchall()
    for row in queryResults:
        print(row)
        album = row[0]
    c.close()
    return album

@eel.expose
def get_next_song(song_id):
    conn = sqlite3.connect('MusicLibrary.db')
    c = conn.cursor()
    query = ("""select path, id from tracks where id = (select min(id) from tracks where id > ?)""")
    c.execute(query, (song_id,))
    queryResults = c.fetchall()
    for row in queryResults:
        print("Query result:", row)
        next_track = row[0]
        next_id = row[1]
    c.close()
    return [next_track, next_id]
    
@eel.expose
def get_song(id):
    conn = sqlite3.connect('MusicLibrary.db')
    c = conn.cursor()
    query = ("""SELECT track_name from tracks where id=?""")
    c.execute(query,(id,))
    queryResults = c.fetchall()
    for row in queryResults:
        print("Query result:", row)
        song = row[0]
    c.close()
    return song

@eel.expose
def get_song_path(id):
    conn = sqlite3.connect('MusicLibrary.db')
    c = conn.cursor()
    query = ("""SELECT path from tracks where id=?""")
    print("id:", id)
    c.execute(query,(id,))
    queryResults = c.fetchall()
    for row in queryResults:
        print("Query result:", row)
        path = row[0].replace("\\", "\\\\")
        print("path: ",path)
    c.close()
    return path


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


    
eel.start('templates/main.html', size=(800, 600))

