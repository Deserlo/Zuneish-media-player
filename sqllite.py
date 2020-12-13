import sqlite3
from sqlite3 import Error
from pathlib import Path

#Loading files
conn = sqlite3.connect('MusicLibrary.db')
data_folder = Path(__file__).parent
home = Path.home()
music_dir = home / "music/"
song_paths = music_dir.rglob("*.mp3")

try:
    
    c = conn.cursor() # The database will be saved in the location where your 'py' file is saved

    # Create table - CLIENTS
    
    #c.execute('''CREATE TABLE artists (artist_name TEXT NOT NULL);''')
    #c.execute('''CREATE TABLE albums (album_name TEXT NOT NULL, artist_id INTEGER NOT NULL, FOREIGN KEY (artist_id) REFERENCES artists (rowid));''')
    #c.execute('''CREATE TABLE tracks (track_name TEXT NOT NULL, album_id INTEGER NOT NULL, FOREIGN KEY (album_id) REFERENCES albums (rowid));''')
    
    #row = c.execute("INSERT INTO artists VALUES ('mos def')").lastrowid

    #c.execute("insert into albums values(?,'black album')"), row )
    count = 1
    for i in song_paths:
        print(str(i))
        c.execute("""INSERT INTO tests (name) VALUES (?);""", [str(i)])
        conn.commit()
        count = count + 1
    

except Error as e:
    print(e)