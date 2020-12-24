import sqlite3
from sqlite3 import Error

class Player(object):
    now_playing_id = 1
    now_playing_path = ""
    now_playing_track_name = ""
    now_playing_album = ""
    now_playing_artist = ""
    
    def update(self, song):
        self.now_playing_id = song[0]
        self.now_playing_path = song[1]
        self.now_playing_track_name = song[2]
        self.now_playing_album = song[3]
        self.now_playing_artist = song[4]
        self.update_player()

    def display(self):
        print(self.now_playing_id)
        print(self.now_playing_path)
        print(self.now_playing_track_name)
        print(self.now_playing_album)
        print(self.now_playing_artist)


    def update_player(self):
        conn = sqlite3.connect('MusicLibrary.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        stmt = ("""UPDATE player SET id=?, path=?, track_name=?, album=?, artist=?""")
        c.execute(stmt,(self.now_playing_id, self.now_playing_path, self.now_playing_track_name, self.now_playing_album, self.now_playing_artist))
        conn.commit()
        c.close()


    def get_last_session(self):
        conn = sqlite3.connect('MusicLibrary.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        query = ("""SELECT * FROM player""")
        c.execute(query)
        queryResult = c.fetchone()
        c.close()
        id, path, track_name, album, artist = queryResult['id'], queryResult['path'].replace("\\", "\\\\"), queryResult['track_name'], queryResult['album'], queryResult['artist']
        print (id, path, track_name, album, artist)
        return [id, path, track_name, album, artist]



