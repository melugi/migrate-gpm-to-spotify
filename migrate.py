import constants
import json
import spotipy
from os import path
from gmusicapi import Mobileclient as GpmClient
from spotipy.oauth2 import SpotifyOAuth

gpm_client = GpmClient()

if not path.exists(constants.CREDS):
  gpm_client.perform_oauth(constants.CREDS)

gpm_client.oauth_login(GpmClient.FROM_MAC_ADDRESS, constants.CREDS)
gpm_artists = []

## Retrieve songs and filter down to unique artists
if gpm_client.is_authenticated():
  songs = gpm_client.get_all_songs()

  for song in songs:
    if song["artist"] not in gpm_artists:
      gpm_artists.append(song["artist"])
else:
  raise Exception("GpmClient is not authenticated. Credentials may have expired, delete and retry.")

gpm_artists.sort()
print(gpm_artists)



