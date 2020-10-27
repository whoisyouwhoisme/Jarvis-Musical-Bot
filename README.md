# Jarvis Telegram Musical Bot for Spotify
This **Telegram** bot allows the user to authorize their **Spotify** account and get cool features.

**[TRY IT!](https://t.me/JarvisMusicalBot "TRY IT!")**

Authorization practically does not collect any private data, except user nickname.


## Its features:
- Now playing. Displaying track cover, title, artists, duration, and searches for a clip for the song in YouTube.
- Super Shuffle. Spotify-alghoritms-less. Just shuffles songs from Liked Songs section many times.
- Your Tops. Displays the tops of songs / artists for a certain period of time. Shows changes in the top, which tracks listened more often, less often, or what new tracks appeared in the tops. You can create a playlist from tops of top songs.
- Music Quiz. Music quiz from Liked Songs / Your Tops.
- Multi-Language. Support English and Russian languages.

## To install the bot:
**1.** Install modules for the bot (Requires Python 3+):

    $ pip install pyTelegramBotAPI
    $ pip install Flask
    $ pip install gevent
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
###### Authorization
![Now Playing](https://github.com/Koteyk0o/Jarvis-Musical-Bot/blob/master/screenshots/auth.png?raw=true "Authorization")
###### Language changing
![Now Playing](https://github.com/Koteyk0o/Jarvis-Musical-Bot/blob/master/screenshots/language%20select.png?raw=true "Language changing")
###### Now Playing
![Now Playing](https://github.com/Koteyk0o/Jarvis-Musical-Bot/blob/master/screenshots/now%20playing.png?raw=true "Now Playing")
###### Super Shuffle
![Super Shuffle](https://github.com/Koteyk0o/Jarvis-Musical-Bot/blob/master/screenshots/super%20shuffle.png?raw=true "Super Shuffle")
###### Top Artists List
![Top Artists](https://github.com/Koteyk0o/Jarvis-Musical-Bot/blob/master/screenshots/top%20artists%20display.png?raw=true "Top Artists")
###### Top Tracks List
![Top Tracks List](https://github.com/Koteyk0o/Jarvis-Musical-Bot/blob/master/screenshots/top%20tracks%20display.png?raw=true "Top Tracks List")
###### Top Tracks Playlist
![Top Tracks Playlist](https://github.com/Koteyk0o/Jarvis-Musical-Bot/blob/master/screenshots/top%20tracks%20playlist.png?raw=true "Top Tracks Playlist")
###### YouTube Clips
![YouTube Clips](https://github.com/Koteyk0o/Jarvis-Musical-Bot/blob/master/screenshots/youtube%20clip.png?raw=true "YouTube Clips")
###### Music Quiz
![Music Quiz](https://github.com/Koteyk0o/Jarvis-Musical-Bot/blob/master/screenshots/music%20quiz.png?raw=true "Music Quiz")
