'''
from this response: https://stackoverflow.com/questions/75286588/spotify-web-api-call-gives-wrong-code-python/75292843#75292843
'''


from flask import Flask, request, redirect, url_for, session
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import requests
from requests import post, get
import json
from dotenv import load_dotenv, find_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
REDIRECT_URI = 'http://127.0.0.1:3000/callback' # my case is 'http://localhost:3000/callback'
#CLIENT_ID = "<your client id>"
#CLIENT_SECRET = "<your client secret>"
SCOPE = [
    "user-read-email",
    "playlist-read-collaborative",
    "user-read-playback-state",
    "user-library-read"
]
app.secret_key = "aljsutnHk47slks$ksiH"         # this is used to encode the session information
app.config['SESSION_COOKIE_NAME'] = 'spotify_track_info_app_cookie'
# the following are for session veriables
TOKEN_INFO = "token_info"
REFRESH_TOKEN_INFO = "refresh_token_info"



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
    '''
    This worked, mostly
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
    '''

    #get_current_track(new_token)

    '''
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
    
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    

    #return json.dumps(res.json())
    session[TOKEN_INFO] = token_info            # wasthis_res_json         # was new_token
    #session[REFRESH_TOKEN_INFO] = refresh_token
    return redirect(url_for('show_track', _external=True))


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        redirect_uri = 'http://127.0.0.1:3000/callback',
        scope = SCOPE           # was "user-library-read"
    )

@app.route("/show_track", methods=['GET'])
def show_track():
    try:
        token_info = get_token()
    except:
        print("The user is not logged in. Redirecting to login page")
        redirect("/login")
    sp = spotipy.Spotify(auth=token_info['access_token'])

    #this_resp = sp.current_user_playing_track()
    this_resp = sp.current_playback()
    #print(f"this response: {this_resp}")

    print(f"\nThe keys: {this_resp['item'].keys()}\n")



    try:
        #resp_json = this_resp.json()
        #print(f"The json response is {resp_json}")

        track_id = this_resp['item']['id']
        print(f"\nTrack ID: {track_id}\n")
        track_name = this_resp['item']['name']
        artists = this_resp['item']['artists']
        artist_name = ', '.join([artist['name'] for artist in artists])
        link = this_resp['item']['external_urls']['spotify']

        current_track_info = {
            "id": track_id,
            "name": track_name,
            "artists": artist_name,
            "link": link
        }
        #return current_track_info
        deets = f"Now Playing: <br>{track_name}<br>by {artist_name}"
        return f"""
            <meta http-equiv="refresh" content="3" /> 
            {deets}"""      # <br>The current time is {}.""".format(datetime.strftime(datetime.now(), "%d %B %Y %X"))
    except:
        return "There is nothing playing at this time"
    
    #return sp.current_user_saved_tracks(limit=50, offset=0)        # this worked
    return sp.current_user_playing_track()
    #return sp.current_playback(market=None, additional_types=None)
    #return sp.current_playback()
    #return sp.current_user_saved_tracks(limit=50, offset=0) 

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    print(f"Token Info is {token_info}")
    # TODO
    return token_info


if __name__ == '__main__':
    global CLIENT_ID
    global CLIENT_SECRET

    _ = load_dotenv(find_dotenv())
    
    CLIENT_SECRET = os.environ.get('SPOTIFY_KEY')
    CLIENT_ID  = os.environ.get('SPOTIFY_ID')
    app.run(port=3000,debug=True)

'''
sp.current_playback() returns the folowing:
{'device': {'id': '216f9d09c85b3e2e56c341fe76e96acb8001ba45', 'is_active': True, 'is_private_session': False, 'is_restricted': False, 'name': 'iPhone', 'supports_volume': False, 'type': 'Smartphone', 'volume_percent': 100}, 
'shuffle_state': False, 
'smart_shuffle': False, 
'repeat_state': 'off', 
'is_playing': True, 
'timestamp': 1753373351623, 
'context': {'external_urls': {'spotify': 'https://open.spotify.com/playlist/21dkzi1BzCJ3thWMKYeCFV'}, 
        'href': 'https://api.spotify.com/v1/playlists/21dkzi1BzCJ3thWMKYeCFV', 
        'type': 'playlist', 
        'uri': 'spotify:playlist:21dkzi1BzCJ3thWMKYeCFV'}, 
        'progress_ms': 305932, 
        'item': {'album': {'album_type': 'album', 
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/58r1rB5t3VF5X6yXGPequV'}, 'href': 'https://api.spotify.com/v1/artists/58r1rB5t3VF5X6yXGPequV', 'id': '58r1rB5t3VF5X6yXGPequV', 'name': 'Maverick City Music', 'type': 'artist', 'uri': 'spotify:artist:58r1rB5t3VF5X6yXGPequV'}, {'external_urls': {'spotify': 'https://open.spotify.com/artist/107CG0UhUl9GJnPwF83N63'}, 'href': 'https://api.spotify.com/v1/artists/107CG0UhUl9GJnPwF83N63', 'id': '107CG0UhUl9GJnPwF83N63', 'name': 'UPPERROOM', 'type': 'artist', 'uri': 'spotify:artist:107CG0UhUl9GJnPwF83N63'}], 
                'available_markets': ['AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DK', 'DO', 'DE', 'EC', 'EE', 'SV', 'FI', 'FR', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'IE', 'IT', 'LV', 'LT', 'LU', 'MY', 'MT', 'MX', 'NL', 'NZ', 'NI', 'NO', 'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'SG', 'SK', 'ES', 'SE', 'CH', 'TW', 'TR', 'UY', 'US', 'GB', 'AD', 'LI', 'MC', 'ID', 'JP', 'TH', 'VN', 'RO', 'IL', 'ZA', 'SA', 'AE', 'BH', 'QA', 'OM', 'KW', 'EG', 'MA', 'DZ', 'TN', 'LB', 'JO', 'PS', 'IN', 'BY', 'KZ', 'MD', 'UA', 'AL', 'BA', 'HR', 'ME', 'MK', 'RS', 'SI', 'KR', 'BD', 'PK', 'LK', 'GH', 'KE', 'NG', 'TZ', 'UG', 'AG', 'AM', 'BS', 'BB', 'BZ', 'BT', 'BW', 'BF', 'CV', 'CW', 'DM', 'FJ', 'GM', 'GE', 'GD', 'GW', 'GY', 'HT', 'JM', 'KI', 'LS', 'LR', 'MW', 'MV', 'ML', 'MH', 'FM', 'NA', 'NR', 'NE', 'PW', 'PG', 'PR', 'WS', 'SM', 'ST', 'SN', 'SC', 'SL', 'SB', 'KN', 'LC', 'VC', 'SR', 'TL', 'TO', 'TT', 'TV', 'VU', 'AZ', 'BN', 'BI', 'KH', 'CM', 'TD', 'KM', 'GQ', 'SZ', 'GA', 'GN', 'KG', 'LA', 'MO', 'MR', 'MN', 'NP', 'RW', 'TG', 'UZ', 'ZW', 'BJ', 'MG', 'MU', 'MZ', 'AO', 'CI', 'DJ', 'ZM', 'CD', 'CG', 'IQ', 'LY', 'TJ', 'VE', 'ET', 'XK'], 
                'external_urls': {'spotify': 'https://open.spotify.com/album/5cqTGnTR7shuPCA2FqyFtR'}, 
                'href': 'https://api.spotify.com/v1/albums/5cqTGnTR7shuPCA2FqyFtR', 
                'id': '5cqTGnTR7shuPCA2FqyFtR', 
                'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab67616d0000b273ad29a40953b33e52530e399e', 'width': 640}, {'height': 300, 'url': 'https://i.scdn.co/image/ab67616d00001e02ad29a40953b33e52530e399e', 'width': 300}, {'height': 64, 'url': 'https://i.scdn.co/image/ab67616d00004851ad29a40953b33e52530e399e', 'width': 64}], 
                'name': 'Move Your Heart', 
                'release_date': '2021-01-29', 
                'release_date_precision': 'day', 
                'total_tracks': 7, 
                'type': 'album', 
                'uri': 'spotify:album:5cqTGnTR7shuPCA2FqyFtR'}, 
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/58r1rB5t3VF5X6yXGPequV'}, 'href': 'https://api.spotify.com/v1/artists/58r1rB5t3VF5X6yXGPequV', 'id': '58r1rB5t3VF5X6yXGPequV', 'name': 'Maverick City Music', 'type': 'artist', 'uri': 'spotify:artist:58r1rB5t3VF5X6yXGPequV'}, {'external_urls': {'spotify': 'https://open.spotify.com/artist/107CG0UhUl9GJnPwF83N63'}, 'href': 'https://api.spotify.com/v1/artists/107CG0UhUl9GJnPwF83N63', 'id': '107CG0UhUl9GJnPwF83N63', 'name': 'UPPERROOM', 'type': 'artist', 'uri': 'spotify:artist:107CG0UhUl9GJnPwF83N63'}, {'external_urls': {'spotify': 'https://open.spotify.com/artist/1bdnGJxkbIIys5Jhk1T74v'}, 'href': 'https://api.spotify.com/v1/artists/1bdnGJxkbIIys5Jhk1T74v', 'id': '1bdnGJxkbIIys5Jhk1T74v', 'name': 'Brandon Lake', 'type': 'artist', 'uri': 'spotify:artist:1bdnGJxkbIIys5Jhk1T74v'}, {'external_urls': {'spotify': 'https://open.spotify.com/artist/0vUp0HrA2d7mcExuf5Wbo6'}, 'href': 'https://api.spotify.com/v1/artists/0vUp0HrA2d7mcExuf5Wbo6', 'id': '0vUp0HrA2d7mcExuf5Wbo6', 'name': 'Eniola Abioye', 'type': 'artist', 'uri': 'spotify:artist:0vUp0HrA2d7mcExuf5Wbo6'}], 'available_markets': ['AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DK', 'DO', 'DE', 'EC', 'EE', 'SV', 'FI', 'FR', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'IE', 'IT', 'LV', 'LT', 'LU', 'MY', 'MT', 'MX', 'NL', 'NZ', 'NI', 'NO', 'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'SG', 'SK', 'ES', 'SE', 'CH', 'TW', 'TR', 'UY', 'US', 'GB', 'AD', 'LI', 'MC', 'ID', 'JP', 'TH', 'VN', 'RO', 'IL', 'ZA', 'SA', 'AE', 'BH', 'QA', 'OM', 'KW', 'EG', 'MA', 'DZ', 'TN', 'LB', 'JO', 'PS', 'IN', 'BY', 'KZ', 'MD', 'UA', 'AL', 'BA', 'HR', 'ME', 'MK', 'RS', 'SI', 'KR', 'BD', 'PK', 'LK', 'GH', 'KE', 'NG', 'TZ', 'UG', 'AG', 'AM', 'BS', 'BB', 'BZ', 'BT', 'BW', 'BF', 'CV', 'CW', 'DM', 'FJ', 'GM', 'GE', 'GD', 'GW', 'GY', 'HT', 'JM', 'KI', 'LS', 'LR', 'MW', 'MV', 'ML', 'MH', 'FM', 'NA', 'NR', 'NE', 'PW', 'PG', 'PR', 'WS', 'SM', 'ST', 'SN', 'SC', 'SL', 'SB', 'KN', 'LC', 'VC', 'SR', 'TL', 'TO', 'TT', 'TV', 'VU', 'AZ', 'BN', 'BI', 'KH', 'CM', 'TD', 'KM', 'GQ', 'SZ', 'GA', 'GN', 'KG', 'LA', 'MO', 'MR', 'MN', 'NP', 'RW', 'TG', 'UZ', 'ZW', 'BJ', 'MG', 'MU', 'MZ', 'AO', 'CI', 'DJ', 'ZM', 'CD', 'CG', 'IQ', 'LY', 'TJ', 'VE', 'ET', 'XK'], 'disc_number': 1, 'duration_ms': 337152, 'explicit': False, 'external_ids': {'isrc': 'TCAFI2167747'}, 'external_urls': {'spotify': 'https://open.spotify.com/track/0A402ZdxwQzaVdyH5Zav5X'}, 'href': 'https://api.spotify.com/v1/tracks/0A402ZdxwQzaVdyH5Zav5X', 'id': '0A402ZdxwQzaVdyH5Zav5X', 'is_local': False, 'name': 'Rest on Us (feat. Brandon Lake & Eniola Abioye)', 'popularity': 72, 'preview_url': None, 'track_number': 1, 'type': 'track', 'uri': 'spotify:track:0A402ZdxwQzaVdyH5Zav5X'}, 'currently_playing_type': 'track', 'actions': {'disallows': {'resuming': True}}}
'''