class Album(object):
    def __init__(self, name, artist, img):
        self.name = name
        self.artist = artist
        self.img = img
    def __hash__(self):
        return hash((self.name, self.artist))
    def __eq__(self, other):
        return (self.name == other.name and self.artist == other.artist)