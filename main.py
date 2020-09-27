import eel
from AudioTrack import AudioTrack
from pathlib import Path
from pygame import mixer
from jinja2 import Environment, FileSystemLoader
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from io import BytesIO
from PIL import Image

paused = False

#Jinja template
file_loader = FileSystemLoader('web/templates')
env = Environment(loader=file_loader)
template = env.get_template('index.html')



#Directory to look for mp3 files
data_folder = Path(__file__).parent
music_dir = data_folder / "music/"
song_paths = music_dir.rglob("*.mp3")


#Mp3 Metadata
def getMutagenTags(path):
    """"""
    audio = ID3(path)
    #print(audio.pprint())
    print ("Artist: %s" % audio['TPE1'].text[0])
    print ("Album: %s" % audio['TALB'].text[0])
    print ("Track: %s" % audio["TIT2"].text[0])
    print ("Release Year: %s" % audio["TDRC"].text[0])



#Storing list of AudioTrack objectors
#  to output to template on starting Eel
tracks = []
artists = set()
albums = set()
size = 100, 100
for i in song_paths:
    #getMutagenTags(i)
    tags = ID3(i)
    #pict = tags.get('APIC:').data
    #im = Image.open(BytesIO(pict))
    #im.thumbnail(size)
    #im.save(i.name + ".thumbnail", "JPEG")
    #print('Picture size : ' + str(im.size))
    album = tags['TALB'].text[0]
    artist = tags['TPE1'].text[0]
    albums.add(album)
    artists.add(artist)
    track = AudioTrack(name=i.name, file_path=i)
    tracks.append(track)


#Jinja template rendering
output = template.render(tracks=tracks, albums=albums, artists=artists)
rendered_filename = data_folder / 'web' / 'templates' / 'main.html'
with open(rendered_filename, "w") as f:
    f.write(output)


eel.init('web')

@eel.expose
def get_song(name):
    print ("Getting first song from directory...")
    '''
    top_level_py_files = Path("src").glob("*.py")
    all_py_files = Path("src").rglob("*.py")
    '''
    #dict {key=songName, value=songPath}
    print(name)
    for t in tracks:
        if t.name == name:
            filepath = t.path
    print (filepath)
    return str(filepath)

@eel.expose
def play_song(songName):
    if paused:
        unpause_song()
    else:
        # Starting the mixer 
        mixer.init() 
        
        # Loading the song 
        song = get_song(songName)
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

