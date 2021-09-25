import flask
import requests
import base64
import json
import os
import random
from dotenv import find_dotenv, load_dotenv
#from requests.api import get

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
    authHeader['authorization'] = "Basic " + base64_message
    authData['grant_type'] = "client_credentials"
    
    res = requests.post(authUrl, headers=authHeader, data=authData)
    #print(res)

    
    responseObject = res.json()
    #print(json.dumps(responseObject, indent=2))

    accessToken = responseObject['access_token']
    
    return accessToken

def getSongInfo(token, random_Artists): 
    SongInfoEndpoint = f"https://api.spotify.com/v1/artists/{random_Artists}/top-tracks?market=US"

    getHeader = {
        "Authorization": f"Bearer {token}" 

    }

    res = requests.get(SongInfoEndpoint, headers= getHeader)

    #print(res.text)
    #print(res.status_code)

    SongInfoObject = res.json()

    return SongInfoObject



#API request
token = getAccessToken(clientID, clientSecret)

artistsID = [
   "3TVXtAsR1Inumwj472S9r4",              #drake
   "2YZyLoL8N0Wb9xBt1NhZWg",             #kendrick lamar
   "6TIYQ3jFPwQSRmorSezPxX",            #machine gun kelly
    "4dpARuHxo51G3z768sgnrY",            #adele 
    "6l3HvQ5sa6mXTsMTB19rO5",           #jcole
]

random_Artists = random.choice(artistsID) #artist info is randomly chosen

songInfo = getSongInfo(token, random_Artists)


#for i in range(1):
songName = songInfo['tracks'][1]['name']
    
artistName = (songInfo['tracks'][1]['artists'][0]['name'])
songImage  = (songInfo['tracks'][1]['album']['images'][0]['url'])
songPreview = (songInfo['tracks'][1]['preview_url'])
   

#Genius Access token
GeniusAccessToken = os.getenv("GeniusAccessToken")

def getGeniusinfo():
    search_term = songName
    genius_search_url = f"http://api.genius.com/search?q={search_term}&access_token={GeniusAccessToken}"
    
    
    res = requests.get(genius_search_url)
    geniusInfoObject = res.json()

    return geniusInfoObject

geniusInfo = getGeniusinfo()



songLyric = geniusInfo['response']['hits'][0]['result']['url']
print(songLyric)

#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app = flask.Flask(__name__)
@app.route("/")
def index():
    
    return flask.render_template("index.html", songName = songName, artistName = artistName, songImage = songImage, songPreview = songPreview, songLyric = songLyric)

app.run(use_reloader = True, debug=True, host='0.0.0.0',port=int(os.getenv('PORT', 8080)),)