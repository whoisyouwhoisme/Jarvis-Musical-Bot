import sqlite3

bot_Database = sqlite3.connect("bot_Database.db")
database_Cursor = bot_Database.cursor()

database_Cursor.execute("""CREATE TABLE bot_Users
                        (telegram_ID TEXT,
                        user_Unique_ID TEXT,
                        language_Select TEXT,
                        bot_Version REAL,
                        user_Position TEXT,
                        reg_Timestamp INTEGER)
                        """)

database_Cursor.execute("""CREATE TABLE spotify_Users
                        (user_Unique_ID TEXT,
                        user_Spotify_ID TEXT,
                        user_Nickname TEXT,
                        spotify_Code TEXT,
                        spotify_Auth_Token TEXT,
                        spotify_Refresh_Token TEXT,
                        auth_Timestamp INTEGER,
                        refresh_Timestamp INTEGER)
                        """)

database_Cursor.execute("""CREATE TABLE users_TopTracks
                        (user_Unique_ID TEXT,
                        topTracks_Data TEXT,
                        refresh_Timestamp INTEGER)
                        """)

database_Cursor.execute("""CREATE TABLE users_TopArtists
                        (user_Unique_ID TEXT,
                        topArtists_Data TEXT,
                        refresh_Timestamp INTEGER)
                        """)

bot_Database.commit()