import requests
import json
from os import path
from gmusicapi import Mobileclient

client = Mobileclient()
creds_file = "./credentials"
log_file = "./log.txt"

if not path.exists(creds_file):
  client.perform_oauth(creds_file)

client.oauth_login(Mobileclient.FROM_MAC_ADDRESS, creds_file)
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

print(artists)

