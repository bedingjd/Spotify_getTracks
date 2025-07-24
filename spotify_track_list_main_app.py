'''
Retrieves the current Track info for display
based on Spotify API Ref Docs here: https://developer.spotify.com/documentation/web-api/reference/get-the-users-currently-playing-track
also based on this example: https://www.youtube.com/watch?v=WAmEZBEeNmg
and info here: https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow
'''



'''
python3 -m venv path/to/venv
    python3 -m venv venv
source path/to/venv/bin/activate
    source venv/bin/activate
python3 spotify_track_list_main_app.py
python3 -m pip install xyz
   or
python3 -m pip install -r requirements.txt      # re: https://pip.pypa.io/en/stable/user_guide/#requirements-files
'''

import os                                       # used for file info and key info
from dotenv import load_dotenv, find_dotenv     # for retrieving key info from .env file
import base64
from requests import post, get
import requests
import json



def get_token(id, key):
    # base64 encode
    auth_string = id + ":" + key
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
        "scope": "user-read-playback-state"
    }

    data = {"grant_type": "client_credentials"}

    result = post(url, headers = headers, data = data)

    json_result = json.loads(result.content)

    token = json_result["access_token"]
    expires_in = json_result["expires_in"]

    return token, expires_in



def get_auth_header(token):
    return {"Authorization": "Bearer " + token}



def get_current_track(token):
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = get_auth_header(token)
    query_url = url

    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)

    print(f"json is {json_result}")

    return



def get_current_track_2(token, client_id, client_key):
    # from https://www.youtube.com/watch?v=yKz38ThJWqE
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = get_auth_header(token)
    #scope = "user-read-playback-state"
    #data = {"grant_type": "client_credentials"}
    data = {"grant_type": "authorization_code"}
    payload = {
        'grant_type': 'authorization_code',
        'code': token,
        'redirect_uri': 'http://localhost:3000',
        'client_id': client_id,
        'client_secret': client_key,
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

    return current_track_info



def get_current_track_3(token):
    # from https://www.youtube.com/watch?v=yKz38ThJWqE
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = get_auth_header(token)
    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
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

    return current_track_info



if __name__ == "__main__":
    # get the id and the key
    _ = load_dotenv(find_dotenv())
    client_key = os.environ.get('SPOTIFY_KEY')
    client_id = os.environ.get('SPOTIFY_ID')

    # get an authorization token
    token, expires_in = get_token(client_id, client_key)
    print(f"My token is: {token}")
    print(f"it expires in: {expires_in}")

    # get the current track
    #get_current_track(token)
    current_track_info = get_current_track_2(token, client_id, client_key)
    print(f"Current Track info is: {current_track_info}")


