from lyrics import get_timestamp_lyric, fetch_parsed_lyrics
from song import Song
from spotify_client import create_spotify_client

sp = create_spotify_client()
current_song = Song(sp.currently_playing())
print("Playing",current_song.name)
lyrics = fetch_parsed_lyrics(current_song.name, current_song.artists)
previous_lyric = get_timestamp_lyric(lyrics, current_song.progress)

while True:
    current_song = Song(sp.currently_playing())

    l = get_timestamp_lyric(lyrics, current_song.progress)[1]

    if not previous_lyric == l:
        print(l)
        previous_lyric = l