**To use the spotify-lyrics app, you will need to provide a client id to connect to the spotify api.**

To get yours, first naviagate to the [spotify developer portal](https://developer.spotify.com/) and log in at the top right corner.


Then, go the [dashboard](https://developer.spotify.com/dashboard) and create an app.

Give it any name and description you want, and leave the "website" section empty.

Then, in the "Redirect URI" section, enter `http://localhost:8888/callback`.

In the "Which API/SDKs are you planning to use?" section, select "Web API".

Once your app is created, open the app settings.

Finally, under "basic information", you'll see your client id.

You then have to copy it and write it in the `settings.ini` file, like so
```
[spotify]
client_id = <your client id>
redirect_uri = http://localhost:8888/callback
```
