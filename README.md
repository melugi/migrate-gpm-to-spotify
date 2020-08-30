# About

This project came about because Google decided to shut down their Play Music service and replace it with YouTube Music. YouTube Music wasn't up to snuff with what I wanted out of a music service, so I made the switch to Spotify. Migrating 600+ artists and 1000+ albums was taking too long though so I wrote this script to alleviate some of the work.

Thus far only artist migration is supported. Album migration might be added but the Play Music service is being cut shortly so the usefulness is debatable.

# Installation, Setup, and Execution

To use the script clone it and initialize a virtualenv with the following version:
```bash
λ  python --version
Python 3.8.2
```

Then run `pip install -r requirements.txt`.

Once dependencies are installed you'll have to generate a Client ID and a Client Secret from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/). To do so log in, generate a new application, and you'll have the tokens generate on the dashboard. You also need to configure the Redirect URI by clicking edit settings and entering the Redirect URI you want to use. I recommend `https://localhost:8080`.

Once you've generated both tokens and added the Redirect URI, configure them in `constants.py` for the script to use. The last bit of configuration required is the Client User constant which corresponds to the username of the account you want to migrate arists to.

The migration scripts can now be executed with `py migrate-*.py`.
