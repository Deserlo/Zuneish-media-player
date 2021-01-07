# Sqlite
import sqlite3
from sqlite3 import Error
import sqllite

from classes.AudioTrack import AudioTrack
from classes.Album import Album



def get_sql_connection():
    conn = sqlite3.connect('music/sqllitedb/MusicLibrary.db')
    return conn


def get_sql_query(name):
    sql = { 
        "now": """SELECT * FROM tracks WHERE id=?""",
        "next": """SELECT * FROM tracks WHERE id = (SELECT min(id) FROM tracks WHERE id > ?)""",
        "previous": """SELECT * FROM tracks WHERE id = (SELECT max(id) FROM tracks WHERE id < ?)""",
        "all": """SELECT track_name, path, album, artist, id FROM tracks order by id asc limit 550;""",
        "update_player": """UPDATE player SET id=?, path=?, track_name=?, album=?, artist=?""",
        "player_status": """SELECT * FROM player"""
    }
    return sql[name]

def db_song_query(order, id):
    conn = get_sql_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor() 
    query = get_sql_query(order)
    c.execute(query, (id,))
    queryResult = c.fetchone()
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


def db_get_player_status():
    conn = get_sql_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    query = get_sql_query("player_status")
    c.execute(query)
    queryResult = c.fetchone()
    c.close()
    id, path, track_name, album, artist = queryResult['id'], queryResult['path'], queryResult['track_name'], queryResult['album'], queryResult['artist']
    return [id, path, track_name, album, artist]


def db_update_player_status(values):
    conn = get_sql_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    stmt = get_sql_query("update_player")
    c.execute(stmt,(values[0], values[1], values[2], values[3], values[4]))
    conn.commit()
    c.close()
    


