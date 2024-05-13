from datetime import timedelta
import syncedlyrics

def get_timestamp_lyric(lyrics, timestamp:timedelta):
    for i, (lyric_timestamp, lyric) in enumerate(lyrics):
        if lyric_timestamp > timestamp:
            return (i-1, lyrics[i-1][1])
    return (i-1, "")

def parse_lrc(lrc:str):
    if lrc == None:
        return None

    try:
        lyrics = [(timedelta(milliseconds=0), " ")]

        for line in lrc.split("\n"):
            line = line.split(" ", maxsplit=1)

            if line == [""] or line == [] or not len(line) == 2:
                continue
            
            time_str = line[0]
            lyric = line[1]

            time_str = time_str.replace("[", "").replace("]", "").replace(".", ":")

            minutes, seconds, centiseconds = map(int, time_str.split(':'))

            lyrics.append((timedelta(minutes=minutes, seconds=seconds, milliseconds=centiseconds*10), lyric))

        return lyrics

    except Exception as exc:
        print(exc)
        return None

def fetch_lrc(song_name:str, artist:str, allow_plain_format=False):
    search_term = song_name+" "
    if type(artist) is list:
        search_term += artist[0]
    elif type(artist) is str:
        search_term += artist

    return syncedlyrics.search(search_term=search_term, allow_plain_format=allow_plain_format)

def fetch_parsed_lyrics(song_name:str, artist:str, allow_plain_format=False):
    return parse_lrc(fetch_lrc(song_name=song_name, artist=artist, allow_plain_format=allow_plain_format))

def ad_lyrics():
    return [(timedelta(milliseconds=0), "A Spotify ad is playing"), (timedelta(days=10**3), " ")]