from configparser import ConfigParser

def reset_default_configs():
    config = ConfigParser(allow_no_value=True)

    config.add_section("theme")
    config.set("theme", "; Available themes: https://ttkbootstrap.readthedocs.io/en/latest/themes/")
    config.set("theme", "theme", "cyborg")

    config.add_section("spotify")
    config.set("spotify", "client_id", "b5669bfe2b1f433db0fe1717aa7576ef")
    config.set("spotify", "redirect_uri", "http://localhost:8888/callback")

    with open("settings.ini", "w") as f:
        config.write(f)

config = ConfigParser(allow_no_value=True)
config.read("settings.ini")

CLIENT_ID = config.get("spotify", "client_id")
REDIRECT_URI = config.get("spotify", "redirect_uri")

theme = config.get("theme", "theme")