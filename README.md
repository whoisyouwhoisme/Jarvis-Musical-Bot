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
**1.** Setting up WebHook:

Because the bot uses WebHook to receive updates, you will need an SSL certificate and a web server (a web server that processes HTTPS and redirects data to the Bot web server)

You can rewrite a code to convert the bot to the polling method (when the bot will constantly poll the Telegram servers for updates).
In this case, you need to rewrite some code in the **bot_Mothership.py** file, you can also remove the useless code for WebHook in the **web_Server.py** file, and remove the **wsgi.py** entry point

You will have to figure out the WebHook configuration yourself, because solution will depend on whether you are using a self-signed certificate, a domain, and how you launch the bot.

In my case, I use the ***nginx+gunicorn+Flask*** bundle to handle web requests.
Nginx provides a secure SSL connection using certificates that are signed by Let's Encrypt, to use **Let's Encrypt**, you must buy a domain name.
The **wsgi.py** file is the entry point for *Gunicorn*.

After you have configured a secure SSL connection, you must tell the Telegram servers where to send updates requests.
The request is created using a CURL request (In this example, the option for the Let's Encrypt certificate, which **nginx** uses)

`curl -F "url=https://YOUR-DOMAIN-NAME/telegram_Api?secret=TELEGRAM-API-TOKEN" "https://api.telegram.org/botTELEGRAM-API-TOKEN/setwebhook"`

Replace YOUR-DOMAIN-NAME, and TELEGRAM-API-TOKEN, and make request.

The result of a successful WebHook connection will be the response:

`{"description": "Webhook was set","ok": true,"result": true}`

**2.** Install modules for the bot (Requires Python 3+):

    $ pip install pyTelegramBotAPI
    $ pip install Flask
    $ pip install google-api-python-client

**3.** After installing the modules, configure **bot_Keys.json:**
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
**4.** After that, run the **database_Creator.py** file which will create the sqlite3 database.

**5.** And just start the bot (2 files, bot, and authorization server):

    $ python bot_Mothership.py
    $ python web_Server.py

## Screenshots
###### Authorization
![Authorization](https://github.com/Koteyk0o/Jarvis-Musical-Bot/blob/master/screenshots/auth.png?raw=true "Authorization")
###### Interface
![Interface](https://github.com/Koteyk0o/Jarvis-Musical-Bot/blob/master/screenshots/interface.png?raw=true "Authorization")
###### Language changing
![Language Changing](https://github.com/Koteyk0o/Jarvis-Musical-Bot/blob/master/screenshots/language%20select.png?raw=true "Language changing")
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
###### Music Quiz
![Music Quiz](https://github.com/Koteyk0o/Jarvis-Musical-Bot/blob/master/screenshots/music%20quiz.png?raw=true "Music Quiz")
