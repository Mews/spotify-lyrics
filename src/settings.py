from configparser import ConfigParser

def reset_default_configs():
    config = ConfigParser(allow_no_value=True)

    config.add_section("theme")
    config.set("theme", "; Available themes: https://ttkbootstrap.readthedocs.io/en/latest/themes/")
    config.set("theme", "theme", "cyborg")

    config.add_section("spotify")
    config.set("spotify", "client_id", "<Your client id>")
    config.set("spotify", "redirect_uri", "http://localhost:8888/callback")
    config.set("spotify", "client_secret", "")

    config.add_section("lyrics")
    config.set("lyrics", "empty_lyric_replacement", chr(int("266B", 16)))

    with open("settings.ini", "w", encoding="utf-8") as f:
        config.write(f)

config = ConfigParser(allow_no_value=True)
config.read("settings.ini", encoding="utf-8")

CLIENT_ID = config.get("spotify", "client_id")
REDIRECT_URI = config.get("spotify", "redirect_uri")
CLIENT_SECRET = config.get("spotify", "client_secret") or None

theme = config.get("theme", "theme")

empty_lyric_replacement = config.get("lyrics", "empty_lyric_replacement")