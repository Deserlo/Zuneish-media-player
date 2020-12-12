import sqlite3
from sqlite3 import Error
from pathlib import Path

conn = sqlite3.connect('MusicLibrary.db')

try:
    
    c = conn.cursor() # The database will be saved in the location where your 'py' file is saved

    # Create table - CLIENTS
    
    #c.execute('''CREATE TABLE artists (artist_name TEXT NOT NULL);''')
    #c.execute('''CREATE TABLE albums (album_name TEXT NOT NULL, artist_id INTEGER NOT NULL, FOREIGN KEY (artist_id) REFERENCES artists (rowid));''')
    #c.execute('''CREATE TABLE tracks (track_name TEXT NOT NULL, album_id INTEGER NOT NULL, FOREIGN KEY (album_id) REFERENCES albums (rowid));''')
    
    #row = c.execute("INSERT INTO artists VALUES ('mos def')").lastrowid

    #c.execute("insert into albums values(?,'black album')"), row )
    count = 1
    query = ("""SELECT * FROM tests order by name asc limit 10;""")
    c.execute(query)
    queryResults = c.fetchall()
    for row in queryResults:
        print (row)

    c.close()
    

except Error as e:
    print(e)