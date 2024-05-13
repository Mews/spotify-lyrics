from datetime import timedelta
from PIL import Image, ImageDraw, ImageOps
import requests
from io import BytesIO

class NoSongFound():
    def __init__(self):
        self.type = "nosong"
        self.is_playing = True
        self.progress = timedelta(milliseconds=0)
        
        self.id = ""
        self.artists = [""]
        self.name = "Waiting for Spotify to start playing"
        self.length = timedelta(milliseconds=1)
    
    def get_image(self, edge_radius=0):
        image = Image.open("assets/default.png").convert("RGBA")

        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0,0) + image.size, radius=edge_radius, fill=255)

        image = ImageOps.fit(image, mask.size, centering=(0.5,0.5))
        image.putalpha(mask)

        return image


class Song():
    def __init__(self, raw_data):
        self.raw_data = raw_data

        self.type = raw_data["currently_playing_type"] #can be "ad" or "track"
        self.is_playing = raw_data["is_playing"]
        self.progress = timedelta(milliseconds=raw_data["progress_ms"])

        if self.type == "ad":
            self.id = "ad"
            self.artists = ["Spotify"]
            self.name = "Advertisement"
            self.length = timedelta(seconds=30)
        
        elif self.type == "track":
            self.id = raw_data["item"]["id"]
            self.artists = self.get_artist_names()
            self.name = raw_data["item"]["name"]
            self.length = timedelta(milliseconds=raw_data["item"]["duration_ms"])

    def get_artist_names(self):
        artist_names = []

        artists = self.raw_data["item"]["artists"]

        for artist_data in artists:
            artist_names.append(artist_data["name"])
        
        return artist_names
    
    def get_image(self, edge_radius=0):
        if self.type == "ad":
            image = Image.open("assets/default.png")
        
        else:
            available_images = self.raw_data["item"]["album"]["images"]

            max_height = -1

            for image in available_images:
                if image["height"] > max_height:
                    max_height = image["height"]
                    highest_quality_image = image
            
            image_data = requests.get(highest_quality_image["url"]).content
            image = Image.open(BytesIO(image_data))

            image = image.resize((max_height, max_height))

        image = image.convert("RGBA")

        if edge_radius == 0:
            return image
        
        else:
            mask = Image.new("L", image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle((0,0) + image.size, radius=edge_radius, fill=255)

            image = ImageOps.fit(image, mask.size, centering=(0.5,0.5))
            image.putalpha(mask)

            return image