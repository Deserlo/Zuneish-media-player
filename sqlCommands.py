# Sqlite
import sqlite3
from sqlite3 import Error
import sqllite

from AudioTrack import AudioTrack
from Album import Album


params = {"id": 1 }

def get_sql_connection():
    conn = sqlite3.connect('MusicLibrary.db')
    return conn


def get_sql_query(name):
    sql = { 
        "now": """SELECT * FROM tracks WHERE id=?""",
        "next": """SELECT * FROM tracks WHERE id = (SELECT min(id) FROM tracks WHERE id > ?)""",
        "previous": """SELECT * FROM tracks WHERE id = (SELECT max(id) FROM tracks WHERE id < ?)""",
        "all": """SELECT track_name, path, album, artist, id FROM tracks order by id asc limit 350;"""
    }
    return sql[name]

def db_song_query(order, id):
    conn = get_sql_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor() 
    query = get_sql_query(order)
    c.execute(query, (id,))
    queryResult = c.fetchone()
    print(queryResult)
    id, path, track_name, album, artist = queryResult['id'], queryResult['path'], queryResult['track_name'], queryResult['album'], queryResult['artist']
    c.close()
    return [id, path, track_name, album, artist]


def db_load_all_songs():
    tracks = []
    artists = set()
    albums = set()
    conn = get_sql_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor() 
    query = get_sql_query('all')
    c.execute(query)
    queryResults = c.fetchall()
    for row in queryResults:  
        track = AudioTrack(id=row[4], name=row[0], album=row[2], artist=row[3], file_path=row[1].replace("\\", "\\\\"))
        tracks.append(track)
        album = Album(name=row[2], artist=row[3], img=row[2] + ".thumbnail")
        albums.add(album)
        artists.add(row[3])
    c.close()
    return [tracks, artists, albums]

