import eel
from pathlib import Path
from mutagen import File
from pygame import mixer

data_folder = Path(__file__).parent
music_dir = data_folder / "music/"
song_list = list(music_dir.rglob("*.mp3"))
print(song_list)
print(song_list[0])
'''
top_level_py_files = Path("src").glob("*.py")
all_py_files = Path("src").rglob("*.py")
'''
file = song_list[0]
filename = str(file)

eel.init('web')

paused = False

@eel.expose
def play_song():
    if paused:
        unpause_song()
    else:
        # Starting the mixer 
        mixer.init() 
        
        # Loading the song 
        print("Loading", filename)
        mixer.music.load(filename) 
        
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
    

eel.start('index.html', size=(800, 600), position=(0,0))

