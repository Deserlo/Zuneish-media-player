import eel
from pathlib import Path
from mutagen import File
from pygame import mixer



eel.init('web')


paused = False
data_folder = Path(__file__).parent
music_dir = data_folder / "music/"
song_paths = music_dir.rglob("*.mp3")
song_list = []
for i in song_paths:
    song_list.append(i.name)


@eel.expose
def show_song():   
    return song_list[0]

@eel.expose
def get_song_filename():
    print ("Getting first song from directory...")
    '''
    top_level_py_files = Path("src").glob("*.py")
    all_py_files = Path("src").rglob("*.py")
    '''
    file = song_list[0]
    filename = str(file)
    return filename

@eel.expose
def play_song():
    if paused:
        unpause_song()
    else:
        # Starting the mixer 
        mixer.init() 
        
        # Loading the song 
        print("Loading", get_song_filename())
        mixer.music.load(get_song_filename()) 
        
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

