import eel
from AudioTrack import AudioTrack
from Album import Album
from pathlib import Path
from pygame import mixer
from jinja2 import Environment, FileSystemLoader
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from io import BytesIO
from PIL import Image
import sqlite3
from sqlite3 import Error


conn = sqlite3.connect('MusicLibrary.db')
c = conn.cursor() 

paused = False

#Jinja template
file_loader = FileSystemLoader('web/templates')
env = Environment(loader=file_loader)
template = env.get_template('index.html')



#Directory to look for mp3 files
'''
    top_level_py_files = Path("src").glob("*.py")
    all_py_files = Path("src").rglob("*.py")
'''
data_folder = Path(__file__).parent
home = Path.home()
music_dir = home / "music/"
print ("music dir:", music_dir)
#music_dir = data_folder / "music/"
song_paths = music_dir.rglob("*.mp3")



#Mp3 Metadata
def getMutagenTags(path):
    """"""
    audio = ID3(path)
    #print(audio.pprint())
    '''
    print ("Artist: %s" % audio['TPE1'].text[0])
    print ("Album: %s" % audio['TALB'].text[0])
    print ("Track: %s" % audio["TIT2"].text[0])
    print ("Release Year: %s" % audio["TDRC"].text[0])
    '''



#Storing album, artist and track info to lists and sets
# (move to sqlite db)

'''
tracks = []
artists = set()
albums = set()
size = 100, 100
for i in song_paths:
    getMutagenTags(i)
    tags = ID3(i)
    try: 
        pict = tags.get('APIC:').data
        im = Image.open(BytesIO(pict))
        im.thumbnail(size)
        album_title = tags['TALB'].text[0]
        artist = tags['TPE1'].text[0]
        album_art_folder = data_folder / "web/templates/icons/albums/"
        im.save(str(album_art_folder) + '/' + album_title + ".thumbnail", "JPEG" )
        album = Album(name=album_title, img=album_title + ".thumbnail")
        albums.add(album)
        artists.add(artist)
        track = AudioTrack(name=i.name, album=album_title, file_path=i)
        tracks.append(track)
    except:
        pass


#Jinja template rendering
output = template.render(tracks=tracks, albums=albums, artists=artists)
rendered_filename = data_folder / 'web' / 'templates' / 'main.html'
with open(rendered_filename, "w") as f:
    f.write(output)
'''

tracks = []
artists = set()
albums = set()

album1 = Album(name="wattts", img="watts.thumbnail")
album2 = Album(name="watts", img="wattss.thumbnail")
albums.add(album1)
albums.add(album2)
artists.add("keith")
artists.add("watts")

query = ("""SELECT * FROM tests order by name asc limit 80;""")
c.execute(query)
queryResults = c.fetchall()
for row in queryResults:
    print(row)
    id = row[0]
    name = row[1].rsplit("\\", 1)[1]
    file_path = row[1].replace("\\", "\\\\")
    track = AudioTrack(name=name, album="album_title", file_path=file_path)
    tracks.append(track)

c.close()




output = template.render(tracks=tracks, albums=albums, artists=artists)
rendered_filename = data_folder / 'web' / 'templates' / 'main.html'
with open(rendered_filename, "w") as f:
    f.write(output)


eel.init('web')

@eel.expose
def get_album(name):
    print(name)
    for t in tracks:
        if t.name == name:
            album = t.album
        print (album)
        return album



@eel.expose
def play_song(songName):
    if paused:
        unpause_song()
    else:
        # Starting the mixer 
        mixer.init() 
        
        # Loading the song 
        print("Loading..", songName)
        mixer.music.load(songName)
        
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

