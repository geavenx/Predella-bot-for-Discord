import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()
clientId = os.environ['SPOTIPY_CLIENT_ID']
clientSecret = os.environ['SPOTIPY_CLIENT_SECRET']
redirectUri = os.environ['SPOTIPY_REDIRECT_URI']

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientId, client_secret=clientSecret, redirect_uri=redirectUri))

def searchSpotify(query):
        results = sp.search(q=query, type='track')
        track = results['tracks']['items'][0]
        #trackItems = track[0] #['artists']
        trackUrl = track['external_urls']['spotify']
        print(trackUrl)
        
searchSpotify('banco')