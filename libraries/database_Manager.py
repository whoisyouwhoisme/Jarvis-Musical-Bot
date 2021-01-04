import sqlite3
import random
import string
from spotify_Module.spotify_Logger import logger

spotify_Database = sqlite3.connect("bot_Database.db")
database_Cursor = spotify_Database.cursor()



def post_Sql_Query(sql_Query, arguments):
    """
    Выполнение SQL запросов
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
    Генерация уникального 42 символьного ID
    """
    return "".join(random.choice(string.ascii_letters + string.digits) for symbols in range(42))



def search_In_Database(keyword_Search, search_Table, search_Row):
    """
    Поиск по базе данных

    keyword_Search - Ключ поиска

    search_Table - Таблица для которой осуществляется поиск

    search_Row - Столбец в котором осуществляется поиск ключа
    """
    query_Arguments = (str(keyword_Search),)
    get_Query = f"SELECT * FROM {search_Table} WHERE {search_Row} = ?"
    get_Result = post_Sql_Query(get_Query, query_Arguments)
    
    return get_Result



def register_User(user_Telegram_ID, user_Unique_ID, user_Language, current_Bot_Version, reg_Timestamp):
    """
    Регистрация пользователя в базе данных, таблица bot_Users

    user_Telegram_ID - Telegram ID пользователя

    user_Unique_ID - Внутренний уникальный ID пользователя

    user_Language - Язык пользователя

    reg_Timestamp - Временная метка регистрации пользователя
    """
    if not search_In_Database(user_Unique_ID, "bot_Users", "user_Unique_ID"):
        query_Arguments = (str(user_Telegram_ID), str(user_Unique_ID), str(user_Language), float(current_Bot_Version), int(reg_Timestamp),)
        register_Query = "INSERT INTO bot_Users (telegram_ID, user_Unique_ID, language_Select, bot_Version, reg_Timestamp) VALUES (?, ?, ?, ?, ?)"
        post_Sql_Query(register_Query, query_Arguments)



def register_Spotify(user_Unique_ID, user_Spotify_ID, user_Nickname, spotify_Auth_Code, spotify_Auth_Token, spotify_Refresh_Token, auth_Timestamp, refresh_Timestamp):
    """
    Регистрация пользователя в базе данных, таблица spotify_Users

    user_Unique_ID - Внутренний уникальный ID пользователя

    user_Spotify_ID - Уникальный ID пользователя в Spotify

    user_Nickname - Ник пользователя в Spotify

    spotify_Auth_Code - Код для получения первичной авторизации

    spotify_Auth_Token - Токен доступа пользователя

    spotify_Refresh_Token - Токен для обновления токена доступа

    auth_Timestamp - Временная метка регистрации пользователя

    refresh_Timestamp - Временная метка последнего обновления токена
    """
    if not search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID"):
        query_Arguments = (str(user_Unique_ID), str(user_Spotify_ID), str(user_Nickname), str(spotify_Auth_Code), str(spotify_Auth_Token), str(spotify_Refresh_Token), int(auth_Timestamp), int(refresh_Timestamp),)
        register_Query = "INSERT INTO spotify_Users (user_Unique_ID, user_Spotify_ID, user_Nickname, spotify_Code, spotify_Auth_Token, spotify_Refresh_Token, auth_Timestamp, refresh_Timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        post_Sql_Query(register_Query, query_Arguments)



def delete_User(user_Unique_ID, table_For_Delete):
    """
    Удаление пользователя из базы данных по уникальному ID

    user_Unique_ID - Уникальный ID пользователя

    table_For_Delete - Таблица в которой происходит удаление
    """
    query_Arguments = (str(user_Unique_ID),)
    register_Query = f"DELETE FROM {table_For_Delete} WHERE user_Unique_ID = ?"
    post_Sql_Query(register_Query, query_Arguments)



def write_User_Position(user_Telegram_ID, user_Position):
    """
    Записать позицию пользователя в боте

    user_Telegram_ID - Telegram ID пользователя

    user_Position - Позиция пользователя
    """
    query_Arguments = (str(user_Position), int(user_Telegram_ID),)
    register_Query = "UPDATE bot_Users SET user_Position = ? WHERE telegram_ID = ?"
    post_Sql_Query(register_Query, query_Arguments)



def write_User_Language(user_Telegram_ID, user_Language):
    """
    Записать язык пользователя

    user_Telegram_ID - Telegram ID пользователя

    user_Language - Язык пользователя
    """
    query_Arguments = (str(user_Language), int(user_Telegram_ID),)
    register_Query = "UPDATE bot_Users SET language_Select = ? WHERE telegram_ID = ?"
    post_Sql_Query(register_Query, query_Arguments)



def write_User_BotVersion(user_Telegram_ID, bot_Version):
    """
    Записать версию бота пользователя

    user_Telegram_ID - Telegram ID пользователя

    bot_Version - Версия бота
    """
    query_Arguments = (str(bot_Version), int(user_Telegram_ID),)
    register_Query = "UPDATE bot_Users SET bot_Version = ? WHERE telegram_ID = ?"
    post_Sql_Query(register_Query, query_Arguments)



def write_User_TopTracks(user_Unique_ID, data_Period, top_Data):
    """
    Записать строку с топ песнями пользователя

    user_Telegram_ID - Telegram ID пользователя

    data_Period - Период выборки топа (short_term, medium_term, long_term)

    top_Data - Сериализованная строка топ песен
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
    Записать строку с топ исполнителями пользователя

    user_Telegram_ID - Telegram ID пользователя

    data_Period - Период выборки топа (short_term, medium_term, long_term)

    top_Data - Сериализованная строка топ исполнителей
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
    Запись обновленного токена доступа Spotify в базу данных

    user_Unique_ID - Уникальный ID пользователя

    refreshed_Token - Обновленный токен

    refresh_Timestamp - Временная метка последнего обновления токена
    """
    query_Arguments = (str(refreshed_Token), int(refresh_Timestamp), str(user_Unique_ID),)
    register_Query = "UPDATE spotify_Users SET spotify_Auth_Token = ?, refresh_Timestamp = ? WHERE user_Unique_ID = ?"
    post_Sql_Query(register_Query, query_Arguments)



def get_User_Position(user_Telegram_ID):
    """
    Получить позицию пользователя из базы данных
    """
    search_Data = search_In_Database(user_Telegram_ID, "bot_Users", "telegram_ID")
    
    if search_Data:
        user_Position = search_Data[0][4]
        logger.info(f"Get User Position For User {user_Telegram_ID}")
        return user_Position
    
    else:
        logger.info(f"CANNOT Get User Position For User {user_Telegram_ID}, sending value 'undefined_Position'")
        return "undefined_Position"



def get_User_Language(user_Telegram_ID):
    """
    Получить язык пользователя из базы данных
    """
    search_Data = search_In_Database(user_Telegram_ID, "bot_Users", "telegram_ID")

    if search_Data:
        user_Language = search_Data[0][2]
        logger.info(f"Get User Language For User {user_Telegram_ID}")
        return user_Language

    else:
        logger.info(f"Cannot Get User Language, Sending Standart Value For User {user_Telegram_ID}")
        return "ENG"



def get_User_BotVersion(user_Telegram_ID):
    """
    Получить версию бота у пользователя
    """
    search_Data = search_In_Database(user_Telegram_ID, "bot_Users", "telegram_ID")

    if search_Data:
        bot_Version = search_Data[0][3]
        logger.info(f"User {user_Telegram_ID} Bot Version: {bot_Version}")
        return bot_Version

    else:
        logger.info(f"Cannot Get User Bot Version, Sending Standart Value For User {user_Telegram_ID}")
        return 0



def get_User_UniqueID(user_Telegram_ID):
    """
    Получить уникальный ID пользователя из базы данных
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
    Проверить регистрацию в боте
    """
    logger.info(f"Check Bot Reg For User {user_Telegram_ID}")
    return search_In_Database(user_Telegram_ID, "bot_Users", "telegram_ID")



def check_Spotify_Login(user_Telegram_ID):
    """
    Проверить авторизован ли пользователь в Spotify
    """
    logger.info(f"Check Spotify Login For User {user_Telegram_ID}")
    return search_In_Database(get_User_UniqueID(user_Telegram_ID), "spotify_Users", "user_Unique_ID")