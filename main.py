# Allows offline web connectivity
import eel

# Web template engine
from jinja2 import Environment, FileSystemLoader

# Custom classes
from classes.Player import *

# DB
from sqllite.sqlCommands import *
from sqllite.sqllite import *

import collections
from pathlib import Path

from wikipedia import wikisearch
import asyncio


# Jinja templates
file_loader = FileSystemLoader('web/templates')
env = Environment(loader=file_loader)

# Player
player = Player()


# Loads from local db
def load():
    tracks, artists, albums = db_load_all_songs()
    nowPlaying = player.get_last_session()
    player.update(nowPlaying)
    player.display()
    return [nowPlaying, tracks, albums, artists]


def render_template(playStatus, nowPlaying, tracks, albums, artists):
    template = env.get_template("index.html")
    output = template.render(playStatus=playStatus, nowPlayer=nowPlaying,
                             tracks=tracks, albums=albums, artists=artists)
    data_folder = Path(__file__).parent
    rendered_filename = data_folder / 'web' / 'templates' / 'main.html'
    with open(rendered_filename, "w", encoding='utf-8') as f:
        f.write(output)


'''
Eel functions
'''


@eel.expose
def reload():
    nowPlaying, tracks, albums, artists = load()
    if player.get_paused_status() == True:
        playStatus = ["unpause", "&#xE102;"]
        print("paused")
    else:
        playStatus = ["pause", "&#xE103;"]
        print("playing")
    render_template(playStatus, nowPlaying, tracks, albums, artists)


@eel.expose
def get_pop_up_results():
    wikisearch.wiki_page_search()

# Music Player functionalities
# Metadata retrieval from music library


@eel.expose
def get_song(id, order):
    song = db_song_query(order, id)
    return song


@eel.expose
def update_player(song):
    player.update(song)


@eel.expose
def play_song(song, id):
    player.play(song)

    # Queue next song
    nextSong = get_song(id, order="next")
    player.queue(nextSong[1])


@eel.expose
def stop_song():
    mixer.music.stop()
    mixer.music.unload()


@eel.expose
def pause_song():
    player.pause()


@eel.expose
def unpause_song():
    player.unpause()


# Data load
data = load()

playStatus = ["play", "&#xE102;"]
# Output to template
render_template(playStatus, data[0], data[1], data[2], data[3])

# Initializing local webserver
eel.init('web')
eel.start('templates/main.html', port=0, size=(800, 600))
