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

tracks = []
artists = set()
albums = set()

#Mp3 Metadata 
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


def saveAlbumThumb(tags, path, img_format):
    size = 100, 100
    pict = tags.get('APIC:').data
    im = Image.open(BytesIO(pict))
    im.thumbnail(size)
    im.save(path, img_format)


def getAlbumArtPath(tags):
    album_title = tags['TALB'].text[0]
    album_art_folder = data_folder / "web/templates/icons/albums/"
    album_art_path = str(album_art_folder) + "" + album_title + ".thumbnail"
    return album_art_path


def loadTrack(path, track, album, artist):
    try:
        c = conn.cursor()
        c.execute("""INSERT INTO tracks (path, track_name, album, artist) VALUES(?,?,?,?);""", [path, track, album, artist])
        conn.commit()
    except Error as e:
        print(e)


for i in song_paths:
    tags = ID3(i)
    try:
        track = tags['TIT2'].text[0]
        artist = tags['TPE1'].text[0]
        album = tags['TALB'].text[0]
        album_art_path = getAlbumArtPath(tags)
        saveAlbumThumb(tags, album_art_path, "JPEG")
        loadTrack(str(i),track, album, artist)
    except:
        pass





    
    

