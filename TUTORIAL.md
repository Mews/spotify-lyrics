To use the spotify-lyrics app, you will need to provide a client id to connect to the spotify api
---

To get yours, first naviagate to the [spotify developer portal](https://developer.spotify.com/) and log in at the top right corner.

Then, go the [dashboard](https://developer.spotify.com/dashboard) and create an app.

![Create app](https://i.ibb.co/wN1yW31/image.png)

Give it any name and description you want, and leave the "website" section empty.

Then, in the "Redirect URI" section, enter `http://localhost:8888/callback`.

In the "Which API/SDKs are you planning to use?" section, select "Web API".

Your app should look something like this

![App configuration](https://i.ibb.co/kBSSr2C/image.png)\
Press the save button.

Once your app is created, open the app settings.

![Settings](https://i.ibb.co/hdLP0RV/image.png)

Finally, under "basic information", you'll see your client id.

![Client id](https://i.ibb.co/XJ7WmQR/image.png)

You then have to copy it and write it in the `settings.ini` file after downloading the [latest release](https://github.com/Mews/spotify-lyrics/releases), like so
```
[spotify]
client_id = <your client id>
redirect_uri = http://localhost:8888/callback
```
