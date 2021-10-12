"""Server module for music player"""

from base64 import b64encode
from os import listdir
from sys import stderr
from flask.helpers import send_file
from flask.json import jsonify
from composition import Composition, PlayList
from flask import Flask, request, make_response

app = Flask(__name__, static_folder='./frontend/build/static')

playlist_list = []
music = [Composition(name=filename[:-len('.mp3')]) for filename in listdir('./music')]
current_playlist = -1

def playlist_data():
    """Return response with json data of current playlists"""
    return make_response(jsonify({
        'playlists': [playlist.get_data() for playlist in playlist_list],
        'current_playlist': current_playlist
    }), 200)

def music_data():
    """Return base64 data of current music played"""
    if current_playlist == -1 or playlist_list[current_playlist].current_composition is None:
        return make_response(jsonify({
            'state': 'none'
        }), 200)
    file = open(f'./music/{playlist_list[current_playlist].current_composition.play()}.mp3', mode='rb')
    b64code = 'data:audio/mp3;base64,' + b64encode(file.read()).decode('ascii')
    file.close()
    return make_response(jsonify({
        'state': 'ok',
        'data': b64code,
        'name': playlist_list[current_playlist].current_composition.name
    }), 200)

def music_list():
    """Return json data of current avaliable music"""
    return make_response(jsonify({
        'music': [composition.name for composition in music]
    }), 200)

@app.route('/')
def index():
    """Index file"""
    return send_file('frontend/build/index.html')

@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    """Request for route for /create_playlist"""
    name = request.get_json(force=True)['name']
    playlist_list.append(PlayList(name))
    return playlist_data()

@app.route('/remove_playlist', methods=['POST'])
def remove_playlist():
    """Request for route for /remove_playlist"""
    index = request.get_json(force=True)['index']
    global current_playlist
    print(current_playlist, file=stderr)
    if index < current_playlist:
        current_playlist -= 1
    elif index == current_playlist:
        current_playlist = -1
    del playlist_list[index]
    print(current_playlist, file=stderr)
    return playlist_data()

@app.route('/add_composition', methods=['POST'])
def add_composition():
    """Request for route for /add_composition"""
    request_data = request.get_json(force=True)
    playlist_index = request_data['playlist_index']
    music_index = request_data['music_index']
    playlist_list[playlist_index].append(music[music_index])
    return playlist_data()

@app.route('/remove_composition', methods=['POST'])
def remove_composition():
    """Request for route for /remove_composition"""
    request_data = request.get_json(force=True)
    playlist_index = request_data['playlist_index']
    music_index = request_data['music_index']
    playlist_list[playlist_index].remove(music_index)
    return playlist_data()

@app.route('/push_forward', methods=['POST'])
def push_forward():
    """Request for route for /push_forward"""
    request_data = request.get_json(force=True)
    playlist_index = request_data['playlist_index']
    music_index = request_data['music_index']
    playlist_list[playlist_index].push_forward(music_index)
    return playlist_data()

@app.route('/push_back', methods=['POST'])
def push_back():
    """Request for route for /push_back"""
    request_data = request.get_json(force=True)
    playlist_index = request_data['playlist_index']
    music_index = request_data['music_index']
    playlist_list[playlist_index].push_back(music_index)
    return playlist_data()

@app.route('/play_next', methods=['POST'])
def play_next():
    """Request for route for /play_next"""
    if current_playlist != -1:
        playlist_list[current_playlist].next()
    return playlist_data()

@app.route('/play_previous', methods=['POST'])
def play_previous():
    """Request for route for /play_previous"""
    if current_playlist != -1:
        playlist_list[current_playlist].prev()
    return playlist_data()

@app.route('/play', methods=['POST'])
def play():
    """Request for route for /play"""
    request_data = request.get_json(force=True)
    playlist_index = request_data['playlist_index']
    music_index = request_data['music_index']
    playlist_list[playlist_index].play(music_index)
    global current_playlist
    current_playlist = playlist_index
    return playlist_data()

@app.route('/get_music_data', methods=['POST'])
def get_music_data():
    """Request for route for /get_music_data"""
    return music_data()

@app.route('/get_music', methods=['POST'])
def get_music():
    """Request for route for /get_music"""
    return music_list()

@app.route('/get_playlists', methods=['POST'])
def get_playlists():
    """Request for route for /get_playlists"""
    return playlist_data()

if __name__ == "__main__":
    app.run(debug=True)
