import sqlite3
from sqlite3 import Error
from pathlib import Path
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from io import BytesIO
from PIL import Image

#Loading files
conn = sqlite3.connect('MusicLibrary.db')
data_folder = Path(__file__).parent
home = Path.home()
music_dir = home / "music/"
song_paths = music_dir.rglob("*.mp3")


#Mp3 Metadata 
#Needs work
def getMutagenTags(path):
    audio = ID3(path)
    #print(audio.pprint())
    try:
        print ("Artist: %s" % audio['TPE1'].text[0])
        print ("Album: %s" % audio['TALB'].text[0])
        print ("Track: %s" % audio["TIT2"].text[0])
        print ("Release Year: %s" % audio["TDRC"].text[0])
    except:
        print("error")



for i in song_paths:
    getMutagenTags(i)


# use below code to get album art
'''
size = 100, 100
for i in song_paths:
    getMutagenTags(i)
    tags = ID3(i)
    try: 
        pict = tags.get('APIC:').data
        im = Image.open(BytesIO(pict))
        im.thumbnail(size)
        album_title = tags['TALB'].text[0]
        #artist = tags['TPE1'].text[0]
        album_art_folder = data_folder / "web/templates/icons/albums/"
        album_art_path = str(album_art_folder) + '/' + album_title + ".thumbnail"
        im.save(album_art_path, "JPEG" )
        try: 
            c = conn.cursor()
            print(album_art_path)
            c.execute("""INSERT INTO albums (name, album_art_path) VALUES (?,?);""", [album_title, album_art_path])
            conn.commit()
        except Error as e:
            print(e)      
    except:
        pass

'''
tracks = []
artists = set()
albums = set()

#Proving it renders
album1 = Album(name="pic1", img="pic1.thumbnail")
album2 = Album(name="pic2", img="pic2.thumbnail")
albums.add(album1)
albums.add(album2)
artists.add("keith")
artists.add("watts")


    
    

