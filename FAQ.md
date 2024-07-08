# FAQ

The app crashes when I open it
---
There are many reasons why this can be hapenning to you.\
A few things you can try to do to fix it are:
- Ensuring you setup your app exactly according to [the tutorial](TUTORIAL.md)
- Waiting a few seconds until the opened authentication page is fully loaded
- Trying different localhost ports for the redirect uri
  - For example: using `http://localhost:1234/callback` instead of `http://localhost:8888/callback`
  - Don't forget to update your `settings.ini` file accordingly by replacing the `redirect_uri` field with the new uri!
- Deleting the `.cache` file if it's present and trying again
- Authenticating using a client secret
  - To do this, you need to go to the same page where you got your client id from, copy the client secret and add it to the `settings.ini` file in front of `client_secret =`
  - You also need the client id you already added for it to work (you don't need to change it if you already set it up)
> [!CAUTION]
> Unlike your client id, your client secret is very sensitive information. As such you have to be very careful not to share it anywhere, and only use it after trying the other options.

**If all those fail, feel free to [open an issue](https://github.com/Mews/spotify-lyrics/issues/new) or contact me through [my discord!](https://discord.com/users/467268976523739157)**

Why do I need a client id to use the app?
---
Because apps that replace native Spotify functionality are against Spotify's developer terms of service, I am unable to register a client id that could be shared across all users of this app.

Because of this, each user has to supply their own client id to connect to the Spotify web api.

You can find how to get your client id [here.](TUTORIAL.md)

My antivirus is saying this app is a virus
---
Some antivirus programs might wrongly flag this app as a virus.

This is simply because the app is not signed, as doing so can cost upwards of [359$/year](https://shop.certum.eu/data-security/code-signing-certificates/certum-ev-code-sigining.html), and I am both unable and unwilling to pay that amount for a small passion project.

Still, if you're suspicious you can look at the source code for the app in this repository and run it directly, or compile an exe yourself.
