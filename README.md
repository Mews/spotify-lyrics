
# Spotify Lyrics

![Logo](https://i.ibb.co/VYfTNT5/banner-transparent.png)

#### An app that connects to your spotify to show you the lyrics to the song you're listening to live.
#### No premium required!

## Usage

To use the app, simply navigate to the [releases page](https://github.com/Mews/spotify-lyrics/releases), download the latest stable release and open the `spotify lyrics.exe` file!

*Alternatively, if you clone the repository, you can also just run the `main.py` file.*

You can then also change the app's theme by editing the `theme` variable in the `settings.ini` file to [one of the available themes](https://ttkbootstrap.readthedocs.io/en/latest/themes/). For example:


    [theme]
    ; available themes: https://ttkbootstrap.readthedocs.io/en/latest/themes/
    theme = litera


If you have any issues using the app, you can also [open an issue](https://github.com/Mews/spotify-lyrics/issues/new) or contact me through [my discord!](https://discord.com/users/467268976523739157)
## Libraries used
[spotipy](https://github.com/spotipy-dev/spotipy) - To use the Spotify WebAPI

[syncedlyrics](https://github.com/moehmeni/syncedlyrics) - To scrape various websites for lrc format lyrics

[ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap/) - To style the gui