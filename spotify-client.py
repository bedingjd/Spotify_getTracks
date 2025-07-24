'''
from this response: https://stackoverflow.com/questions/75286588/spotify-web-api-call-gives-wrong-code-python/75292843#75292843
'''


from flask import Flask, request, redirect
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import requests
from requests import post, get
import json
from dotenv import load_dotenv, find_dotenv
import os

app = Flask(__name__)

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
REDIRECT_URI = 'http://127.0.0.1:3000/callback' # my case is 'http://localhost:3000/callback'
#CLIENT_ID = "<your client id>"
#CLIENT_SECRET = "<your client secret>"
SCOPE = [
    "user-read-email",
    "playlist-read-collaborative",
    "user-read-playback-state"
]


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def get_current_track(token):
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = get_auth_header(token)
    query_url = url

    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)

    print(f"/n The current track json is {json_result}\n")
    return


@app.route("/login")
def login():
    spotify = OAuth2Session(CLIENT_ID, scope=SCOPE, redirect_uri=REDIRECT_URI)
    authorization_url, state = spotify.authorization_url(AUTH_URL)
    return redirect(authorization_url)

@app.route("/callback", methods=['GET'])
def callback():
    code = request.args.get('code')
    #print(f"Code is {code}")
    res = requests.post(TOKEN_URL,
        auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI
        })
    
    # now that we have the access token, lets get the track info
    this_res_json = res.json()
    #print(f"\nres = {this_res_json}\n")
    allTheKeys = this_res_json.keys()
    #print(f"\nAll the keys: {allTheKeys}\n")
    new_token = this_res_json.get('access_token')
    #print(f"\nThe new access token is {new_token}\n")
    refresh_token = this_res_json.get('refresh_token')

    #new_token = this_res_json["access_token"]
    #refresh_token = this_res_json['refresh_token']

    #get_current_track(new_token)

    
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = get_auth_header(new_token)
    payload = {
        'grant_type': 'authorization_code',
        'code': new_token,
        'redirect_uri': 'http://l127.0.0.1:3000/callback',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    
    response = requests.get(
        url=url,
        headers=headers,
        data=payload
    )
    print(f"Response is {str(response)}")
    '''
    resp_json = response.json()
    print(f"The json response is {resp_json}")

    track_id = resp_json['item']['id']
    track_name = resp_json['item']['name']
    artists = resp_json['item']['artists']
    artist_name = ', '.join([artist['name'] for artist in artists])
    link = resp_json['item']['external_urls']['spotify']

    current_track_info = {
        "id": track_id,
        "name": track_name,
        "artists": artist_name,
        "link": link
    }
    '''
    


    return json.dumps(res.json())

if __name__ == '__main__':
    global CLIENT_ID
    global CLIENT_SECRET

    _ = load_dotenv(find_dotenv())
    
    CLIENT_SECRET = os.environ.get('SPOTIFY_KEY')
    CLIENT_ID  = os.environ.get('SPOTIFY_ID')
    app.run(port=3000,debug=True)