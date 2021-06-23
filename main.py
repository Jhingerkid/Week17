from flask import Flask, render_template, request
import json
import requests

def makeSearchRequest(inputSong):
    url = "https://shazam.p.rapidapi.com/search"
    querystring = {"term": inputSong,
                   "locale": "en-US", "offset": "0", "limit": "10"}
    headers = {
        'x-rapidapi-key': "9b689232b2mshb9760bb5da27bf9p14e4a3jsnda3498b3e945",
        'x-rapidapi-host': "shazam.p.rapidapi.com"
        }
    searchResponse = (requests.request("GET",
                      url, headers=headers, params=querystring).json())
    return searchResponse


def makeRecommendationRequest(selectedKey):
    url = "https://shazam.p.rapidapi.com/songs/list-recommendations"
    querystring = {"key": selectedKey, "locale": "en-US"}
    headers = {
               'x-rapidapi-key':
               "9b689232b2mshb9760bb5da27bf9p14e4a3jsnda3498b3e945",
               'x-rapidapi-host': "shazam.p.rapidapi.com"
    }
    recommendationResponse = (requests.request("GET",
                              url, headers=headers, params=querystring).json())
    return recommendationResponse

def makeSongList(data):
    count = 0
    songList = []
    for x in data:
        songTitle = data[count]['track']['title']
        songArtist = data[count]['track']['subtitle']
        songEntry = songTitle + " by " + songArtist
        songList.append(songEntry)
        count = count + 1
    return songList

def makeSongKeys(data):
    keyCount = 0
    songKeys = []
    for x in data:
        songKey = data[keyCount]['track']['key']
        songKeys.append(songKey)
        keyCount = keyCount + 1
    return songKeys

def parseRecommendedSongs(recSongsRaw):
    recSongPicks = []
    for song in recSongsRaw:
        recSongTitle = song['title']
        recSongArtist = song['subtitle']
        if 'images' in song:
            recSongAlbumCover = song['images']['coverart']
        elif 'images' not in song:
            recSongAlbumCover = "No Album Cover"
        songEntry = recSongTitle + " by " + recSongArtist
        item = {"info" : songEntry, "cover" : recSongAlbumCover}
        recSongPicks.append(item)
    return recSongPicks

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/SongRecommendation", methods=['POST'])
def songrecommendations():
    selectedKey = request.form['songpick']
    recSongsRaw = makeRecommendationRequest(selectedKey)['tracks']
    recSongs = parseRecommendedSongs(recSongsRaw)
    return render_template("songreccomendation.html", recSongs=enumerate(recSongs))

@app.route("/SongSuggestion", methods=['POST'])
def songsuggestions():
    inputSong = request.form['songname']
    songSearch = makeSongList(makeSearchRequest(inputSong)['tracks']['hits'])
    songKeys = makeSongKeys(makeSearchRequest(inputSong)['tracks']['hits'])
    return render_template("songsuggestion.html", songSearch=enumerate(songSearch), songKeys=songKeys)
    
if __name__ == "__main__":
    app.run(debug=True)