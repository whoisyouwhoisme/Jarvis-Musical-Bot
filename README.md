# Jarvis Telegram Musical Bot for Spotify
This **Telegram** bot allows the user to authorize their **Spotify** account and get cool features.

**[TRY IT!](https://t.me/JarvisMusicalBot "TRY IT!")**

Authorization practically does not collect any private data, except user nickname.


## Its features:
- Now playing. Displaying track cover, title, artists, duration.
- Super Shuffle. Spotify-alghoritms-less. Just shuffles songs from Liked Songs section many times
- Your Tops. Displays the tops of songs / artists for a certain period of time. You can create a playlist from tops of top songs.
- YouTube Clip. Search for a clip for the song currently playing. Just one button press.
- Music Quiz. Music quiz from Liked Songs / Your Tops.

## To install the bot:
**1.** Install modules for the bot:

    $ pip install pyTelegramBotAPI
    $ pip install Flask
    $ pip install WSGIserver
    $ pip install google-api-python-client

**2.** After installing the modules, configure **bot_Keys.json:**
```json
{
    "spotify": {
        "client_ID":"YOUR SPOTIFY APP CLIENT ID",
        "client_Secret":"YOUR SPOTIFY APP CLIENT SECRET",
        "redirect_URI":"YOUR SPOTIFY APP REDIRECT URI"
    },
    "telegram": {
        "telegram_Key":"YOUR TELEGRAM API KEY"
    },
    "google": {
        "youTube_Key":"YOUTUBE CONSOLE API KEY"
    }
}
```
**3.** After that, run the **database_Creator.py** file which will create the sqlite3 database.

**4.** And just start the bot (2 files, bot, and authorization server):

    $ python bot_Mothership.py
    $ python auth_Server.py

## Screenshots
![Alt text](/Jarvis-Musical-Bot/screenshots/now playing.png?raw=true)
