import constants
import json
import spotipy
from gmusicapi import Mobileclient as GpmClient
from os import path
from progress.bar import Bar
from spotipy.oauth2 import SpotifyOAuth

## Performs oAuth to gpm and init client
gpm_client = GpmClient()

if not path.exists(constants.GPM_CACHE):
  gpm_client.perform_oauth(constants.GPM_CACHE)

gpm_client.oauth_login(GpmClient.FROM_MAC_ADDRESS, constants.GPM_CACHE)
gpm_artists = []

## Retrieve songs from gpm and reduce down to unique artists
if gpm_client.is_authenticated():
  print("Retrieving songs from GPM...")
  songs = gpm_client.get_all_songs()

  for song in songs:
    if song["artist"] not in gpm_artists:
      gpm_artists.append(song["artist"])
else:
  raise Exception("GpmClient is not authenticated. Credentials may have expired, delete and retry.")

gpm_artists.sort()

## Perform oAuth to Spotify and init client
sp_client = spotipy.Spotify(
  auth_manager=SpotifyOAuth(
    client_id=constants.CLIENT_ID,
    client_secret=constants.CLIENT_SECRET,
    redirect_uri="http://localhost:8080",
    scope=constants.FOLLOW_SCOPE,
    username=constants.CLIENT_USER
    )
  )

artist_ids = []
failed_searches = []
open(constants.LOG, 'w').close()

bar = Bar("Searching artists on Spotify...", max=len(gpm_artists))

for artist in gpm_artists:
  artist_id = ''
  srch_results = sp_client.search(q='artist: ' + artist, type='artist')

  for result in srch_results["artists"]["items"]:
    if result["name"] == artist:
      artist_id = result["id"]
      break
  
  if artist_id != '':
    artist_ids.append(artist_id)
  else:
    with open(constants.LOG, 'a', encoding="utf-8") as log:
      print(f"Failed to find a match for artist: {artist}.", file=log)
    failed_searches.append(artist)
  
  bar.next()

bar.finish()

print("Finished searching artists. See below for results:\n")
print(f"Found {len(artist_ids)}/{len(gpm_artists)} artists. Proceeding to follow them for the user: {constants.CLIENT_USER}.")
print(f"Missed {len(failed_searches)}/{len(gpm_artists)}. See {constants.LOG} for a list of failures.\n")

bar = Bar(f"Following artists for {constants.CLIENT_USER}...", max=len(artist_ids))

for artist_id in artist_ids:
  sp_client.user_follow_artists([artist_id])
  bar.next()

bar.finish()


