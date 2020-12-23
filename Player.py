class Player(object):
    now_playing_id = 1
    now_playing_track = ""
    now_playing_artist = ""
    
    def update(self, now_playing_id, now_playing_track, now_playing_artist):
        self.now_playing_id = now_playing_id
        self.now_playing_track = now_playing_track
        self.now_playing_artist = now_playing_artist

    def display(self):
        print(self.now_playing_id)
        print(self.now_playing_track)
        print(self.now_playing_artist)
