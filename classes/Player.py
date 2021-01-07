import eel

import sqlite3
from sqlite3 import Error
from sqllite.sqlCommands import *

# Music player library
from pygame import mixer



class Player(object):

    now_playing_id = 1
    now_playing_path = ""
    now_playing_track_name = ""
    now_playing_album = ""
    now_playing_artist = ""
    paused = True
    

    def play(self, song):
        self.paused = False

        # Starting the mixer 
        mixer.init() 
        
        # Loading the song 
        print("Loading..", song)
        mixer.music.load(song)
        
        # Setting the volume 
        mixer.music.set_volume(0.7) 
        
        # Start playing the song 
        mixer.music.play() 


    def queue(self, nextSong):
        mixer.music.queue(nextSong)

    def pause(self):
        self.paused = True
        print("pausing song..")
        mixer.music.pause()

    def unpause(self):
        self.paused = False
        print("resuming song..")
        mixer.music.unpause()


    def get_paused_status(self):
        return self.paused

    def update(self, song):
        print("Now playing...", song)
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
        attributes = [self.now_playing_id, self.now_playing_path, self.now_playing_track_name, self.now_playing_album, self.now_playing_artist]
        db_update_player_status(attributes)


    def get_last_session(self):
        id, path, track_name, album, artist = db_get_player_status()
        return [id, path, track_name, album, artist]




