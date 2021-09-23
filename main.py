import flask
import requests
import base64
import json
import os
import random
from dotenv import find_dotenv, load_dotenv
from requests.api import Response

load_dotenv(find_dotenv())

authUrl = "https://accounts.spotify.com/api/token"
authHeader = {}
authData = {}
clientID = os.getenv("clientID")
clientSecret = os.getenv("clientSecret")

#base64 Encode client ID and Client Secret
def getAccessToken(clientID, clientSecret):
    message = f"{clientID}:{clientSecret}"
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    #print(base64_message)
    authData['grant_type'] = "client_credentials"
    authHeader['authorization'] = "Basic " + base64_message
    res = requests.post(authUrl, headers=authHeader, data=authData)
    #print(res)

    
    responseObject = res.json()
    #print(json.dumps(responseObject, indent=2))

    accessToken = responseObject['access_token']
    
    return accessToken

def getSongInfo(token, random_Artists): 
    SongInfoEndpoint = f"https://api.spotify.com/v1/artists/{random_Artists}/top-tracks?market=US"

    getHeader = {
        "Authorization": "Bearer " + token

    }


    res = requests.get(SongInfoEndpoint, headers= getHeader)


    SongInfoObject = res.json()

    return SongInfoObject



#API request
token = getAccessToken(clientID, clientSecret)

artistsID = [
    ""              #drake
    ""              #kendrick lamar
    ""              #machine gun kelly
    ""              #adele 
    ""              #jcole
]

random_Artists = random.choice(artistsID) #artist info is randomly chosen

songInfo = getSongInfo(token, random_Artists)


for i in range(1):
    songName = (songInfo['tracks'][i]['name'])
    artistName = (songInfo['tracks'][i]['artists'][0]['name'])
    songImage  = (songInfo['tracks'][i]['album']['images'][0]['url'])
    songPreview = (songInfo['tracks'][i]['preview_url'])


#Genius Access token
GeniusAccessToken = os.getenv("GeniusAccessToken")

def getGeniusinfo():
    search_term = songName
    genius_search_url = f"http://api.genius.com/search?q={search_term}&access_token={GeniusAccessToken}"
    res = requests.get(genius_search_url)
    geniusInfoObject = res.json

    return geniusInfoObject

geniusInfo = getGeniusinfo()


for i in range(1):
    songLyric = (geniusInfo['response']['hits'][i]['result']['url]'])

    app = flask.Flask(__name__)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    @app.route('/')
    def index():
        print("this is a debug statement")
        return flask.render_template(
            "index.html",
            songName = songName,
            artistName = artistName,
            songImage = songImage,
            songPreview = songPreview,
            songLyric = songLyric
        )

    app.run(
        host=os.getenv('IP', '0.0.0.0')
    )
    port=int(os.getenv('PORT', 8080)),
        
    