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
query = ("""SELECT * FROM tests;""")
c.execute(query)
queryResults = c.fetchall()
for row in queryResults:
    print(row)      
    id = row[0]
    name = row[1].rsplit("\\", 1)[1]
    file_path = row[1].replace("\\", "\\\\")
    track = AudioTrack(name=name, album="album_title", file_path=file_path)
    tracks.append(track)

query1 = ("""select distinct name, album_art_path from albums;""")
c.execute(query1)
queryResults = c.fetchall()
for row in queryResults:
    print(row)
    album_title = row[0]
    album_art_path = row[1].replace("\\", "\\\\")
    album = Album(name=album_title, img=album_title + ".thumbnail")
    albums.add(album)


c.close()


artists.add("temp")

output = template.render(tracks=tracks, albums=albums, artists=artists)
data_folder = Path(__file__).parent
rendered_filename = data_folder / 'web' / 'templates' / 'main.html'
with open(rendered_filename, "w") as f:
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

