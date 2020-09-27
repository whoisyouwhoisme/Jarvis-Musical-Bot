import sqlite3
import random
import string

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



def register_User(user_Telegram_ID, user_Unique_ID, reg_Timestamp):
    """
    Регистрация пользователя в базе данных, таблица bot_Users

    user_Telegram_ID - Telegram ID пользователя

    user_Unique_ID - Внутренний уникальный ID пользователя

    reg_Timestamp - Временная метка регистрации пользователя
    """
    if not search_In_Database(user_Unique_ID, "bot_Users", "user_Unique_ID"):
        query_Arguments = (str(user_Telegram_ID), str(user_Unique_ID), int(reg_Timestamp),)
        register_Query = "INSERT INTO bot_Users (telegram_ID, user_Unique_ID, reg_Timestamp) VALUES (?, ?, ?)"
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