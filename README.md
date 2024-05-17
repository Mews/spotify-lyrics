
# Spotify Lyrics

![Logo](https://i.ibb.co/VYfTNT5/banner-transparent.png)

**An app that connects to your spotify to show you the lyrics to the song you're listening to live.**\
**No premium required!**

## Usage
***To be able to use the app, you will first need to provide a client id to connect to the spotify api.***\
***You can find how to get yours [here](TUTORIAL.md).***

After getting your client id, navigate to the [releases page](https://github.com/Mews/spotify-lyrics/releases) and download the latest release.\
Then, open the `settings.ini` file and write your client id as such
```
[spotify]
client_id = <your client id>
redirect_uri = http://localhost:8888/callback
```
After that, just open the `spotify lyrics.exe` file!

*Some antivirus programs might flag the app as a virus. This is only because the app is not signed, but, if you're suspicious, you can look at the [source code](https://github.com/Mews/spotify-lyrics/tree/main/src) and run the `main.py` file directly, or compile the executable yourself.*

---

You can then also change the app's theme by editing the `theme` variable in the `settings.ini` file to [one of the available themes](https://ttkbootstrap.readthedocs.io/en/latest/themes/). For example, to use the "solar" dark theme:


    [theme]
    ; available themes: https://ttkbootstrap.readthedocs.io/en/latest/themes/
    theme = solar


**If you have any issues using the app, you can also [open an issue](https://github.com/Mews/spotify-lyrics/issues/new) or contact me through [my discord!](https://discord.com/users/467268976523739157)**

## Changelog

| Version | Changes                                                           
|---------|---------------------------------------
| 0.1.0   | Initial release                                                  
| 0.2.0   | Added support for theme and settings editing                           
| 0.3.0   | Updated lrc parser
| 0.4.0   | Fixed issue with window stuttering when moving it around


## Libraries used
[spotipy](https://github.com/spotipy-dev/spotipy) - To use the Spotify WebAPI

[syncedlyrics](https://github.com/moehmeni/syncedlyrics) - To scrape various websites for lrc format lyrics

[ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap/) - To style the gui
