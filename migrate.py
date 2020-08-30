import constants
import json
import spotipy
from os import path
from gmusicapi import Mobileclient

client = Mobileclient()

if not path.exists(constants.CREDS):
  client.perform_oauth(constants.CREDS)

client.oauth_login(Mobileclient.FROM_MAC_ADDRESS, constants.CREDS)
artists = []

## Retrieve songs and filter down to unique artists
if client.is_authenticated():
  songs = client.get_all_songs()

  for song in songs:
    if song["artist"] not in artists:
      artists.append(song["artist"])
else:
  raise Exception("MobileClient is not authenticated. Credentials may have expired, delete and retry.")

artists.sort()


