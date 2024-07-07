import spotipy
from spotipy.oauth2 import SpotifyPKCE, SpotifyOAuth
import settings

SCOPE = "user-read-currently-playing"

def create_spotify_client(scopes:list = [SCOPE]) -> spotipy.Spotify:
    scope_str = ""
    for scope in scopes:
        scope_str += scope
        scope_str += ","
    scope_str = scope_str[:-1]

    if not settings.CLIENT_SECRET:
        print("Authenticating using PKCE")
        auth_manager = SpotifyPKCE(client_id=settings.CLIENT_ID, redirect_uri=settings.REDIRECT_URI, scope=scope_str)
    else:
        print("Authenticating using OAuth")
        auth_manager = SpotifyOAuth(client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET, redirect_uri=settings.REDIRECT_URI, scope=scope_str)

    auth_manager.get_access_token()

    client = spotipy.Spotify(auth_manager=auth_manager)

    return client