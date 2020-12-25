# Allows offline web connectivity
import eel

# Music player library
from pygame import mixer

# Web template engine
from jinja2 import Environment, FileSystemLoader

# Custom classes
from Player import Player

# DB 
from sqlCommands import *

import collections
from pathlib import Path


paused = False


#Jinja templates
file_loader = FileSystemLoader('web/templates')
env = Environment(loader=file_loader)

#Player
player = Player()
player.display()


# Loads from local db
def load():
    tracks, artists, albums = db_load_all_songs()
    nowPlaying = player.get_last_session()
    return [nowPlaying, tracks, albums, artists]
    

    

def render_template(playStatus, nowPlaying, tracks, albums, artists):
    template = env.get_template("index.html")
    output = template.render(playStatus=playStatus, nowPlayer=nowPlaying, tracks=tracks, albums=albums, artists=artists)
    data_folder = Path(__file__).parent
    rendered_filename = data_folder / 'web' / 'templates' / 'main.html'
    with open(rendered_filename, "w", encoding='utf-8') as f:
        f.write(output)




'''
Eel functions
'''
@eel.expose
def reload():
    nowPlaying, tracks, albums, artists = load()
    if paused == True:
        playStatus = [ "unpause", "&#xE102;" ]
        print("paused")
    else:
        playStatus = [ "pause", "&#xE103;" ]
        print("playing")
    render_template(playStatus, nowPlaying, tracks, albums, artists)




#Metadata retrieval from music library
@eel.expose
def get_song(id, order):
    song = db_song_query(order, id)
    return song


@eel.expose
def update_player(song):
    player.update(song)


#Music Player functionalities
@eel.expose
def play_song(song, id):
    # Starting the mixer 
    mixer.init() 
    
    # Loading the song 
    print("Loading..", song)
    mixer.music.load(song)
    
    # Setting the volume 
    mixer.music.set_volume(0.7) 
    
    # Start playing the song 
    mixer.music.play() 

    # Queue next song
    nextSong = get_song(id, "next")
    mixer.music.queue(nextSong[1])



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



# Data load
data = load()

playStatus = ["play", "&#xE102;"]
# Output to template
render_template(playStatus, data[0], data[1], data[2], data[3])

# Initializing local webserver
eel.init('web')  
eel.start('templates/main.html', port=0, size=(800, 600))

