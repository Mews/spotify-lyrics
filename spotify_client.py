import spotipy
from spotipy.oauth2 import SpotifyPKCE
import settings

SCOPE = "user-read-currently-playing"

def create_spotify_client(scopes:list = [SCOPE]) -> spotipy.Spotify:
    scope_str = ""
    for scope in scopes:
        scope_str += scope
        scope_str += ","
    scope_str = scope_str[:-1]

    auth_manager = SpotifyPKCE(client_id=settings.CLIENT_ID, redirect_uri=settings.REDIRECT_URI, scope=scope_str)
    auth_manager.get_access_token()

    client = spotipy.Spotify(auth_manager=auth_manager)

    return client