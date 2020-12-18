import eel
from AudioTrack import AudioTrack
from Album import Album
from pathlib import Path
from pygame import mixer
from jinja2 import Environment, FileSystemLoader
import sqlite3
from sqlite3 import Error


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
query = ("""SELECT path, track_name, album, artist FROM tracks asc limit 200;""")
c.execute(query)
queryResults = c.fetchall()
for row in queryResults:
    print(row)     
    file_path = row[0].replace("\\", "\\\\")
    name = row[1]
    album = row[2]
    artist = row[3]
    track = AudioTrack(name=name, album=album, artist=artist, file_path=file_path)
    tracks.append(track)
    #Need to make album set unique based on name
    ustr = ".thumbnail"
    album = Album(name=album, img=album + ustr)
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
def get_album(song):
    return "Aerosmith"




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

