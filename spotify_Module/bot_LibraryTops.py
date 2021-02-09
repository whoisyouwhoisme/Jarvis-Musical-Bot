import urllib
import json
import math
from spotify_Module import localization
from spotify_Module import bot_Sender
from spotify_Module import spotify_Service
from libraries import database_Manager as db_Manager
from spotify_Module import spotify_Exceptions
from spotify_Module.spotify_Logger import logger



language_Vocabluary = localization.load_Vocabluary()



def to_Main_Menu(user_ID):
    """
    Вернуть пользователя в главное меню
    """
    logger.info(f"Sending Main Menu Keyboard For User {user_ID}")
    db_Manager.write_User_Position(user_ID, "main_Menu")
    user_Language = db_Manager.get_User_Language(user_ID)
    bot_Sender.controls_Main_Menu(user_ID, language_Name=user_Language)



def process_Type_Selector_Message(user_ID, message_Text, user_Language):
    if message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["songs"]:
        bot_Sender.tops_Time_Period(user_ID, language_Name=user_Language)
        db_Manager.write_User_Position(user_ID, "user_TopTracks_Time")

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["artists"]:
        bot_Sender.tops_Time_Period(user_ID, language_Name=user_Language)
        db_Manager.write_User_Position(user_ID, "user_TopArtists_Time")

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"]:
        to_Main_Menu(user_ID)

    else:
        bot_Sender.astray_Notification(user_ID, language_Name=user_Language)



def process_TopSongs_Time_Selector_Message(user_ID, message_Text, user_Language):
    if message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["time_Buttons"]["4_Weeks"]:
        create_TopTracks(user_ID, language_Name=user_Language, time_Range="short_term")

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["time_Buttons"]["6_Months"]:
        create_TopTracks(user_ID, language_Name=user_Language, time_Range="medium_term")

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["time_Buttons"]["all_Time"]:
        create_TopTracks(user_ID, language_Name=user_Language, time_Range="long_term")

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"]:
        to_Main_Menu(user_ID)                

    else:
        bot_Sender.astray_Notification(user_ID, language_Name=user_Language)



def process_TopArtists_Time_Selector_Message(user_ID, message_Text, user_Language):
    if message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["time_Buttons"]["4_Weeks"]:
        create_TopArtists(user_ID, language_Name=user_Language, time_Range="short_term")

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["time_Buttons"]["6_Months"]:
        create_TopArtists(user_ID, language_Name=user_Language, time_Range="medium_term")

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["time_Buttons"]["all_Time"]:
        create_TopArtists(user_ID, language_Name=user_Language, time_Range="long_term")

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"]:
        to_Main_Menu(user_ID)                

    else:
        bot_Sender.astray_Notification(user_ID, language_Name=user_Language)    



def process_TopTracks_List(user_ID, time_Range, list_Page):
    """
    Подготовить данные для новой страницы Топ треков

    user_ID - Telegram ID пользователя

    time_Range - Диапазон времени для выборки (short_term, medium_term, long_term)

    list_Page - Страница списка данных
    """
    database_User_Tracks = db_Manager.search_In_Database(db_Manager.get_User_UniqueID(user_ID), "users_TopTracks", "user_Unique_ID")

    if database_User_Tracks: #Если у пользователя есть топ
        if time_Range == "short_term": #хахах, вот это костыли, вери найс гуд найс
            user_Tracks = database_User_Tracks[0][1]
        elif time_Range == "medium_term":
            user_Tracks = database_User_Tracks[0][2]
        elif time_Range == "long_term":
            user_Tracks = database_User_Tracks[0][3]

    top_Data = json.loads(user_Tracks) #Десериализуем строку в словарь
    max_Pages = math.ceil(len(top_Data["items"]) / 10) #Получаем кол-во страниц
    current_Page = {
        "current_Page":list_Page,
        "max_Pages":max_Pages,
        "time_Range":top_Data["top_Info"]["time_Range"],
        "last_Update":top_Data["top_Info"]["timestamp"],
        "items":{},
    }

    start_Index, stop_Index = ((10 * list_Page) - 10), (10 * list_Page) #ПОВЫШАЕМ ЧИТАЕМОСТЬ!
    for item in range(start_Index, stop_Index):
        if item < len(top_Data["items"]):
            current_Page["items"][item] = {
                "prefix":top_Data["items"][item]["prefix"],
                "artists":top_Data["items"][item]["artists"],
                "name":top_Data["items"][item]["name"]
            }

    return current_Page



def process_TopArtists_List(user_ID, time_Range, list_Page):
    """
    Подготовить данные для новой страницы Топ исполнителей

    user_ID - Telegram ID пользователя

    time_Range - Диапазон времени для выборки (short_term, medium_term, long_term)

    list_Page - Страница списка данных
    """
    database_User_Artists = db_Manager.search_In_Database(db_Manager.get_User_UniqueID(user_ID), "users_TopArtists", "user_Unique_ID")

    if database_User_Artists: #Если у пользователя есть топ
        if time_Range == "short_term": #хахах, вот это костыли, вери найс гуд найс
            user_Artists = database_User_Artists[0][1]
        elif time_Range == "medium_term":
            user_Artists = database_User_Artists[0][2]
        elif time_Range == "long_term":
            user_Artists = database_User_Artists[0][3]

    top_Data = json.loads(user_Artists) #Десериализуем строку в словарь
    max_Pages = math.ceil(len(top_Data["items"]) / 10) #Получаем кол-во страниц
    current_Page = {
        "current_Page":list_Page,
        "max_Pages":max_Pages,
        "time_Range":top_Data["top_Info"]["time_Range"],
        "last_Update":top_Data["top_Info"]["timestamp"],
        "items":{},
    }

    start_Index, stop_Index = ((10 * list_Page) - 10), (10 * list_Page) #ПОВЫШАЕМ ЧИТАЕМОСТЬ!
    for item in range(start_Index, stop_Index):
        if item < len(top_Data["items"]):
            current_Page["items"][item] = {
                "prefix":top_Data["items"][item]["prefix"],
                "artist":top_Data["items"][item]["artist"],
                "followers":top_Data["items"][item]["followers"]
            }

    return current_Page



def create_TopTracks(user_ID, language_Name, time_Range):
    """
    Создать топ треков для пользователя

    user_ID - Telegram ID пользователя

    language_Vocabluary - Словарь языков

    language_Name - Название языка пользователя

    time_Range - Диапазон времени для выборки (short_term, medium_term, long_term)
    """
    try:
        top_Data = spotify_Service.get_User_Top_Tracks(db_Manager.get_User_UniqueID(user_ID), entities_Limit=50, time_Range=time_Range)
        logger.info(f"Get User Top Tracks For User {user_ID}")

    except spotify_Exceptions.no_Tops_Data:
        bot_Sender.insufficient_Data_For_Top(user_ID, language_Name=language_Name)

    except spotify_Exceptions.http_Error:
        bot_Sender.cannot_Authorize(user_ID, language_Name=language_Name)
        logger.error(f"HTTP ERROR OCCURED WHEN PREPARING TOP TRACKS LIST FOR USER {user_ID}")

    except spotify_Exceptions.http_Connection_Error:
        bot_Sender.servers_Link_Error(user_ID, language_Name=language_Name)
        logger.error(f"CONNECTION ERROR OCCURED WHEN PREPARING TOP TRACKS LIST FOR USER {user_ID}")

    except:
        bot_Sender.unknown_Error(user_ID, language_Name=language_Name)
        logger.error(f"UNKNOWN ERROR OCCURED WHEN PREPARING TOP TRACKS LIST FOR USER {user_ID}")

    else:
        db_Manager.write_User_TopTracks(db_Manager.get_User_UniqueID(user_ID), data_Period=time_Range, top_Data=json.dumps(top_Data))

        try:
            bot_Sender.tracks_Top(user_ID, process_TopTracks_List(user_ID, time_Range, 1), language_Name=language_Name)
        
        except:
            bot_Sender.top_Database_Error(user_ID, language_Name=language_Name)
            logger.error(f"DATABASE ERROR OCCURED WHEN PREPARING TOP TRACKS LIST FOR USER {user_ID}")
        
        else:
            logger.info(f"Top Tracks Prepared Successfuly For User {user_ID}")

    finally:
        to_Main_Menu(user_ID)



def create_TopArtists(user_ID, language_Name, time_Range):
    """
    Создать топ исполнителей для пользователя

    user_ID - Telegram ID пользователя

    language_Vocabluary - Словарь языков

    language_Name - Название языка пользователя

    time_Range - Диапазон времени для выборки (short_term, medium_term, long_term)
    """
    try:
        top_Data = spotify_Service.get_User_Top_Artists(db_Manager.get_User_UniqueID(user_ID), entities_Limit=50, time_Range=time_Range)
        logger.info(f"Get User Top Artists For User {user_ID}")

    except spotify_Exceptions.no_Tops_Data:
        bot_Sender.insufficient_Data_For_Top(user_ID, language_Name=language_Name)

    except spotify_Exceptions.http_Error:
        bot_Sender.cannot_Authorize(user_ID, language_Name=language_Name)
        logger.error(f"HTTP ERROR OCCURED WHEN PREPARING TOP ARTISTS LIST FOR USER {user_ID}")

    except spotify_Exceptions.http_Connection_Error:
        bot_Sender.servers_Link_Error(user_ID, language_Name=language_Name)
        logger.error(f"CONNECTION ERROR OCCURED WHEN PREPARING TOP ARTISTS LIST FOR USER {user_ID}")

    except:
        bot_Sender.unknown_Error(user_ID, language_Name=language_Name)
        logger.error(f"UNKNOWN ERROR OCCURED WHEN PREPARING TOP ARTISTS LIST FOR USER {user_ID}")

    else:
        db_Manager.write_User_TopArtists(db_Manager.get_User_UniqueID(user_ID), data_Period=time_Range, top_Data=json.dumps(top_Data))

        try:
            bot_Sender.artists_Top(user_ID, process_TopArtists_List(user_ID, time_Range, 1), language_Name=language_Name)
        
        except:
            bot_Sender.top_Database_Error(user_ID, language_Name=language_Name)
            logger.error(f"DATABASE ERROR OCCURED WHEN PREPARING TOP ARTISTS LIST FOR USER {user_ID}")
        
        else:
            logger.info(f"Top Artists Prepared Successfuly For User {user_ID}")

    finally:
        to_Main_Menu(user_ID)



def create_TopTracks_Playlist(user_ID, language_Name, time_Range):
    """
    Создать плейлист из топ треков для пользователя

    user_ID - Telegram ID пользователя

    language_Vocabluary - Словарь языков

    language_Name - Название языка пользователя

    time_Range - Диапазон времени для выборки (short_term, medium_term, long_term)
    """
    try:
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)

        localization_Data = {
            "playlist_Name":language_Vocabluary[language_Name]["chat_Messages"]["yourTops"]["your_TopSongs"],
            "playlist_TimeRange":language_Vocabluary[language_Name]["chat_Messages"]["yourTops"][time_Range],
            "playlist_Description":language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["playlist_Generated_ByJarvis"],
        }

        playlist_ID = spotify_Service.create_Top_Tracks_Playlist(user_Unique_ID, localization_Data=localization_Data, time_Range=time_Range)
        playlist_Data = spotify_Service.get_Playlist_Data(user_Unique_ID, playlist_ID)
        logger.info(f"Creating Top Tracks Playlist For User {user_ID}")

    except spotify_Exceptions.http_Error:
        bot_Sender.cannot_Authorize(user_ID, language_Name=language_Name)
        logger.error(f"HTTP ERROR OCCURED WHEN PREPARING TOP TRACKS PLAYLIST FOR USER {user_ID}")

    except spotify_Exceptions.http_Connection_Error:
        bot_Sender.servers_Link_Error(user_ID, language_Name=language_Name)
        logger.error(f"CONNECTION ERROR OCCURED WHEN PREPARING TOP TRACKS PLAYLIST FOR USER {user_ID}")

    except:
        bot_Sender.unknown_Error(user_ID, language_Name=language_Name)
        logger.error(f"UNKNOWN ERROR OCCURED WHEN PREPARING TOP TRACKS PLAYLIST FOR USER {user_ID}")

    else:
        playlist_Data["playlist_Cover"] = urllib.request.urlopen(playlist_Data["images"][1]["url"]).read() #Скачивание обложки

        bot_Sender.playlist_Ready(user_ID, playlist_Data, language_Name=language_Name)
        logger.info(f"Top Tracks Playlist Created Successfuly For User {user_ID}")