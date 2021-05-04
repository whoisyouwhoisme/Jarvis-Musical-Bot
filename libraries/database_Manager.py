import sqlite3
import random
import string
from spotify_Module.spotify_Logger import logger

spotify_Database = sqlite3.connect("bot_Database.db")
database_Cursor = spotify_Database.cursor()



def post_Sql_Query(sql_Query, arguments):
    """
    Executing SQL queries
    """
    with sqlite3.connect("bot_Database.db") as connection:
        cursor = connection.cursor()

        try:
            cursor.execute(sql_Query, arguments)
            result = cursor.fetchall()

            return result
        except sqlite3.DatabaseError as Error:
            print("Error: ", Error)
        else:
            spotify_Database.commit()



def generate_Unique_ID():
    """
    Generation of a unique 42 character ID
    """
    return "".join(random.choice(string.ascii_letters + string.digits) for symbols in range(42))



def search_In_Database(keyword_Search, search_Table, search_Row):
    """
    Database search

    keyword_Search - Search Key

    search_Table - The table for which to search

    search_Row - The column in which the key is searched
    """
    query_Arguments = (str(keyword_Search),)
    get_Query = f"SELECT * FROM {search_Table} WHERE {search_Row} = ?"
    get_Result = post_Sql_Query(get_Query, query_Arguments)
    
    return get_Result



def register_User(user_Telegram_ID, user_Unique_ID, user_Language, current_Bot_Version, reg_Timestamp):
    """
    User registration in the database, bot_Users table

    user_Telegram_ID - Telegram user ID

    user_Unique_ID - Internal unique user ID

    user_Language - User language

    reg_Timestamp - User registration timestamp
    """
    if not search_In_Database(user_Unique_ID, "bot_Users", "user_Unique_ID"):
        query_Arguments = (str(user_Telegram_ID), str(user_Unique_ID), str(user_Language), float(current_Bot_Version), int(reg_Timestamp),)
        register_Query = "INSERT INTO bot_Users (telegram_ID, user_Unique_ID, language_Select, bot_Version, reg_Timestamp) VALUES (?, ?, ?, ?, ?)"
        post_Sql_Query(register_Query, query_Arguments)



def register_Spotify(user_Unique_ID, user_Spotify_ID, user_Nickname, spotify_Auth_Code, spotify_Auth_Token, spotify_Refresh_Token, auth_Timestamp, refresh_Timestamp):
    """
    User registration in the database, spotify_Users table

    user_Unique_ID - Internal unique user ID

    user_Spotify_ID - Unique user ID in Spotify

    user_Nickname - Spotify username

    spotify_Auth_Code - Code for getting primary authorization

    spotify_Auth_Token - User access token

    spotify_Refresh_Token - Token for refreshing the access token

    auth_Timestamp - User registration timestamp

    refresh_Timestamp - Timestamp of the last token refresh
    """
    if not search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID"):
        query_Arguments = (str(user_Unique_ID), str(user_Spotify_ID), str(user_Nickname), str(spotify_Auth_Code), str(spotify_Auth_Token), str(spotify_Refresh_Token), int(auth_Timestamp), int(refresh_Timestamp),)
        register_Query = "INSERT INTO spotify_Users (user_Unique_ID, user_Spotify_ID, user_Nickname, spotify_Code, spotify_Auth_Token, spotify_Refresh_Token, auth_Timestamp, refresh_Timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        post_Sql_Query(register_Query, query_Arguments)



def delete_User(user_Unique_ID, table_For_Delete):
    """
    Removing a user from the database by unique ID

    user_Unique_ID - Unique user ID

    table_For_Delete - The table in which the deletion occurs
    """
    query_Arguments = (str(user_Unique_ID),)
    register_Query = f"DELETE FROM {table_For_Delete} WHERE user_Unique_ID = ?"
    post_Sql_Query(register_Query, query_Arguments)



def write_User_Position(user_Telegram_ID, user_Position):
    """
    Record the position of the user in the bot

    user_Telegram_ID - Telegram user ID

    user_Position - User position
    """
    query_Arguments = (str(user_Position), int(user_Telegram_ID),)
    register_Query = "UPDATE bot_Users SET user_Position = ? WHERE telegram_ID = ?"
    post_Sql_Query(register_Query, query_Arguments)



def write_User_Language(user_Telegram_ID, user_Language):
    """
    Record user language

    user_Telegram_ID - Telegram user ID

    user_Language - User language
    """
    query_Arguments = (str(user_Language), int(user_Telegram_ID),)
    register_Query = "UPDATE bot_Users SET language_Select = ? WHERE telegram_ID = ?"
    post_Sql_Query(register_Query, query_Arguments)



def write_User_BotVersion(user_Telegram_ID, bot_Version):
    """
    Record the user's bot version

    user_Telegram_ID - Telegram user ID

    bot_Version - Bot version
    """
    query_Arguments = (str(bot_Version), int(user_Telegram_ID),)
    register_Query = "UPDATE bot_Users SET bot_Version = ? WHERE telegram_ID = ?"
    post_Sql_Query(register_Query, query_Arguments)



def write_User_TopTracks(user_Unique_ID, data_Period, top_Data):
    """
    Record a line with the user's top songs

    user_Telegram_ID - Telegram user ID

    data_Period - Top sampling period (short_term, medium_term, long_term)

    top_Data - Serialized string of top songs
    """
    if not search_In_Database(user_Unique_ID, "users_TopTracks", "user_Unique_ID"):
        query_Arguments = (str(user_Unique_ID),)
        register_Query = "INSERT INTO users_TopTracks (user_Unique_ID) VALUES (?)"
        post_Sql_Query(register_Query, query_Arguments)

    query_Arguments = (str(top_Data), str(user_Unique_ID),)
    register_Query = f"UPDATE users_TopTracks SET {data_Period} = ? WHERE user_Unique_ID = ?"
    post_Sql_Query(register_Query, query_Arguments)



def write_User_TopArtists(user_Unique_ID, data_Period, top_Data):
    """
    Write a line with the user's top performers

    user_Telegram_ID - Telegram user ID

    data_Period - Top sampling period (short_term, medium_term, long_term)

    top_Data - Serialized string of top artists
    """
    if not search_In_Database(user_Unique_ID, "users_TopArtists", "user_Unique_ID"):
        query_Arguments = (str(user_Unique_ID),)
        register_Query = "INSERT INTO users_TopArtists (user_Unique_ID) VALUES (?)"
        post_Sql_Query(register_Query, query_Arguments)

    query_Arguments = (str(top_Data), str(user_Unique_ID),)
    register_Query = f"UPDATE users_TopArtists SET {data_Period} = ? WHERE user_Unique_ID = ?"
    post_Sql_Query(register_Query, query_Arguments)



def write_Refreshed_Token(user_Unique_ID, refreshed_Token, refresh_Timestamp):
    """
    Writing Updated Spotify Access Token to Database

    user_Unique_ID - Unique user ID

    refreshed_Token - Refreshed token

    refresh_Timestamp - Timestamp of the last token refresh
    """
    query_Arguments = (str(refreshed_Token), int(refresh_Timestamp), str(user_Unique_ID),)
    register_Query = "UPDATE spotify_Users SET spotify_Auth_Token = ?, refresh_Timestamp = ? WHERE user_Unique_ID = ?"
    post_Sql_Query(register_Query, query_Arguments)



def get_User_Position(user_Telegram_ID):
    """
    Get user position from database
    """
    search_Data = search_In_Database(user_Telegram_ID, "bot_Users", "telegram_ID")
    
    if search_Data:
        user_Position = search_Data[0][4]

        if user_Position:
            logger.info(f"Get User Position For User {user_Telegram_ID}")
            return user_Position

        else:
            logger.info(f"CANNOT Get User Position For User {user_Telegram_ID}, sending value 'undefined_Position'")
            return "undefined_Position"
    
    else:
        logger.info(f"CANNOT Get User Position For User {user_Telegram_ID}, sending value 'undefined_Position'")
        return "undefined_Position"



def get_User_Language(user_Telegram_ID):
    """
    Get user language from database
    """
    search_Data = search_In_Database(user_Telegram_ID, "bot_Users", "telegram_ID")

    if search_Data:
        user_Language = search_Data[0][2]

        if user_Language:
            logger.info(f"Get User Language For User {user_Telegram_ID}")
            return user_Language

        else:
            logger.info(f"Cannot Get User Language, Sending Standart Value For User {user_Telegram_ID}")
            return "ENG"
    
    else:
        logger.info(f"Cannot Get User Language, Sending Standart Value For User {user_Telegram_ID}")
        return "ENG"



def get_User_BotVersion(user_Telegram_ID):
    """
    Get the bot version from the user
    """
    search_Data = search_In_Database(user_Telegram_ID, "bot_Users", "telegram_ID")

    if search_Data:
        bot_Version = search_Data[0][3]

        if bot_Version:
            logger.info(f"User {user_Telegram_ID} Bot Version: {bot_Version}")
            return bot_Version
        
        else:
            logger.info(f"Cannot Get User Bot Version, Sending Standart Value For User {user_Telegram_ID}")
            return 0

    else:
        logger.info(f"Cannot Get User Bot Version, Sending Standart Value For User {user_Telegram_ID}")
        return 0



def get_User_UniqueID(user_Telegram_ID):
    """
    Get a unique user ID from the database
    """
    search_Data = search_In_Database(user_Telegram_ID, "bot_Users", "telegram_ID")

    if search_Data:
        user_UniqueID = search_Data[0][1]
        logger.info(f"Get User Unique ID For User {user_Telegram_ID}")
        return user_UniqueID
    
    else:
        logger.error(f"CANNOT Get User Unique ID For User {user_Telegram_ID}")
        return None



def check_Bot_Reg(user_Telegram_ID):
    """
    Check registration in the bot
    """
    logger.info(f"Check Bot Reg For User {user_Telegram_ID}")
    return search_In_Database(user_Telegram_ID, "bot_Users", "telegram_ID")



def check_Spotify_Login(user_Telegram_ID):
    """
    Check if a user is logged in to Spotify
    """
    logger.info(f"Check Spotify Login For User {user_Telegram_ID}")
    return search_In_Database(get_User_UniqueID(user_Telegram_ID), "spotify_Users", "user_Unique_ID")