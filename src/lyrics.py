import re
from datetime import timedelta
import syncedlyrics

def get_timestamp_lyric(lyrics, timestamp:timedelta):
    for i, (lyric_timestamp, lyric) in enumerate(lyrics):
        if lyric_timestamp > timestamp:
            return (i-1, lyrics[i-1][1])
    return (i-1, "")

def str_to_timestamp(timestamp_str):
    timestamp_str = timestamp_str.replace("[","").replace("]","").replace(".", ":")

    minutes, seconds, centiseconds = map(int, timestamp_str.split(':'))

    timestamp = timedelta(minutes=minutes, seconds=seconds, milliseconds=centiseconds*10)

    return timestamp

def parse_lrc(lrc_string:str):
    TIMESTAMP_REGEX = "\\[[^\\]]*\\]"
    pattern = re.compile(TIMESTAMP_REGEX)

    parsed_lyrcs = []

    try:
        if "\n" in lrc_string:
            # Separate lines format

            for line in lrc_string.split("\n"):
                match_ = pattern.search(line)

                if match_ == None:
                    continue
                
                timestamp_str = match_.group()

                timestamp = str_to_timestamp(timestamp_str)

                lyric = line.replace(match_.group(), "").strip()

                parsed_lyrcs.append((timestamp, lyric))
        
        else:
            # No line break format
            
            matches = pattern.finditer(lrc_string)

            str_indexes = []
            timestamps = [timedelta(milliseconds=0)]

            for match_ in matches:
                str_indexes.append(match_.span()[0])

                timestamp_str = match_.group()
                timestamps.append(str_to_timestamp(timestamp_str))

            c_index = 0

            for i, index in enumerate(str_indexes):
                lyric = lrc_string[c_index:index].strip()
                timestamp = timestamps[i]

                c_index = index + 10

                parsed_lyrcs.append((timestamp, lyric))

    except Exception as exc:
        print(exc)
        return None
        
    return (None if parsed_lyrcs == [] else parsed_lyrcs)

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