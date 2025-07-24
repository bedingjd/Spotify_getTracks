# Spotify_getTracks
a little app to retrieve the currently playing Spotify track information, using the Spotify API

## Set-up
1. Create a virtual environment
  > Generally: python3 -m venv path/to/venv <br>
  > python3 -m venv venv
2. Activate the virtual environment
  > Generally: source path/to/venv/bin/activate <br>
  > source venv/bin/activate
3. Install any needed requirements
  a. via the requirements file provided
    > python3 -m pip install -r requirements.txt      
    Details about using a requirements file From this [source](https://pip.pypa.io/en/stable/user_guide/#requirements-files)
  b. or install them individually
    >   python3 -m pip install xyz
4. Go to the Spotify creator [Dashboard](https://developer.spotify.com/dashboard), and set-up the app (see tutorials)
5. Create a ```.env``` file (no extension).  Inside the file place your keys copied from the Spotify Dashboard:
  > SPOTIFY_ID = "your-key-here" <br>
  > SPOTIFY_KEY = "your-key-here"
6. Start the flask app
  > python3 spotify-client.py


## To Run
- Activate the virtual environment
> source venv/bin/activate
- Start the flask app
> python3 spotify-client.py


## References
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- [Spotify API Documentation Getting Started](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)
- [Spotify API Documentation to get the current track](https://developer.spotify.com/documentation/web-api/reference/get-the-users-currently-playing-track)
- [Good Stack overflow answer on authentication](https://stackoverflow.com/questions/75286588/spotify-web-api-call-gives-wrong-code-python/75292843#75292843)
- 

- Some other API libraries, not from Spotify
  - [https://www.google.com/search?client=safari&rls=en&q=spotify+api+python&ie=UTF-8&oe=UTF-8](https://www.google.com/search?client=safari&rls=en&q=spotify+api+python&ie=UTF-8&oe=UTF-8)
  - [Spotipy](https://spotipy.readthedocs.io/en/2.25.1/#spotipy.client.Spotify.current_playback)
  - [Flask Quickstart](https://flask.palletsprojects.com/en/stable/quickstart/)

- Tutorials
  - [Python Spotify API #1 - Everything You Need To Know About OAuth2](https://youtu.be/g6IAGvBZDkE?si=0LZwpoin-MlKs7qz)
  - [Python Spotify API #2 - Setting Up The Endpoints](https://youtu.be/XZA_s-vfGKQ?si=66SyO5tTKWF7wYzh)
  - [Python Spotify API #3 - Retrieving Users Songs](https://youtu.be/1TYyX8soQ8M?si=1Zk96E3YTvICWv6L)
  - [Spotify OAuth: Automating Discover Weekly Playlist - Full Tutorial](https://youtu.be/mBycigbJQzA?si=tsHK3dfPPPfZ79w1)
  - [Spotify Overlay (current song) with Python!](https://youtu.be/BzSFbrVDwFc?si=cKU-tYGEGg7sb_ps)
  - [How to use Spotify's API with Python](https://www.youtube.com/watch?v=WAmEZBEeNmg)
  - [Get Currently Playing Track with Spotify API](https://www.youtube.com/watch?v=yKz38ThJWqE)
  

- Other examples
  - [https://github.com/AcrobaticPanicc/Spotify-Playlist-Generator1/tree/master](https://github.com/AcrobaticPanicc/Spotify-Playlist-Generator1/tree/master)
  - [https://github.com/spotify/web-api-examples](https://github.com/spotify/web-api-examples)


  ## TO DO
  - [ ] Format the output so that the information fills the screen, and the background can be removed via chromakey
  - [ ] Add logic (from Part 3 tutorial) to refresh the token upon expiration
