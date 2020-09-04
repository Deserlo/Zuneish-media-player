import eel
from mutagen import File
from pygame import mixer

file = r"C:\Users\18054\MyProjects\zune-ish\music\01 - Shak'em Loose Tonight.mp3"
eel.init('web')



@eel.expose
def play_song():
    # Starting the mixer 
    mixer.init() 
    
    # Loading the song 
    mixer.music.load(file) 
    
    # Setting the volume 
    mixer.music.set_volume(0.7) 
    
    # Start playing the song 
    mixer.music.play() 

@eel.expose
def stop_song():
    mixer.music.stop()

@eel.expose
def pause_song():
    mixer.music.pause()

eel.start('main.html', size=(800, 600), position=(0,0))

