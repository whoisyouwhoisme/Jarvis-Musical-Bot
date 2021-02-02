import urllib
from spotify_Module import bot_Spotify_Sender
from spotify_Module import localization
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
    bot_Spotify_Sender.controls_Main_Menu(user_ID, language_Name=user_Language)



def in_Work(user_ID):
    """
    Поставить пользователю позицию in Work
    """
    logger.info(f"Sending In Work State For User {user_ID}")
    db_Manager.write_User_Position(user_ID, "work_In_Progress")
    user_Language = db_Manager.get_User_Language(user_ID)
    bot_Spotify_Sender.playlist_Preparing(user_ID, language_Name=user_Language)



def process_SuperShuffle_Message(user_ID, message_Text, user_Language):
    if message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["offset_Size"]["100_Songs"]:
        create_SuperShuffle(user_ID, language_Name=user_Language, tracks_Count=100)

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["offset_Size"]["200_Songs"]:
        create_SuperShuffle(user_ID, language_Name=user_Language, tracks_Count=200)

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["offset_Size"]["all_Offset"]:
        create_SuperShuffle(user_ID, language_Name=user_Language)

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"]:
        to_Main_Menu(user_ID)
    
    else:
        bot_Spotify_Sender.astray_Notification(user_ID, language_Name=user_Language)



def create_SuperShuffle(user_ID, language_Name, tracks_Count=None):
    """
    Создать супер-шаффл для пользователя

    user_ID - Telegram ID пользователя

    tracks_Count - Количество треков для супер-шафла (необязательный параметр, если параметра нет - выбираются все песни из Liked Songs)
    """
    try:
        in_Work(user_ID)
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)

        localization_Data = {
            "playlist_Name":language_Vocabluary[language_Name]["chat_Messages"]["superShuffle"]["your_SuperShuffle"],
            "playlist_Description":language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["playlist_Generated_ByJarvis"],
        }
    
        spotify_Service.check_User_Liked_Songs(user_Unique_ID, 100)
        playlist_ID = spotify_Service.super_Shuffle(user_Unique_ID, localization_Data=localization_Data, tracks_Count=tracks_Count)
        playlist_Data = spotify_Service.get_Playlist_Data(user_Unique_ID, playlist_ID)
        
        logger.info(f"Creating Super Shuffle For User {user_ID}")

    except spotify_Exceptions.no_Tracks:
        bot_Spotify_Sender.insufficient_Data_For_Shuffle(user_ID, language_Name=language_Name)

    except spotify_Exceptions.http_Error:
        bot_Spotify_Sender.cannot_Authorize(user_ID, language_Name=language_Name)
        logger.error(f"HTTP ERROR OCCURED WHEN PREPARING SUPER SHUFFLE FOR USER {user_ID}")

    except spotify_Exceptions.http_Connection_Error:
        bot_Spotify_Sender.servers_Link_Error(user_ID, language_Name=language_Name)
        logger.error(f"CONNECTION ERROR OCCURED WHEN PREPARING SUPER SHUFFLE FOR USER {user_ID}")

    except:
        bot_Spotify_Sender.unknown_Error(user_ID, language_Name=language_Name)
        logger.error(f"UNKNOWN ERROR OCCURED WHEN PREPARING SUPER SHUFFLE FOR USER {user_ID}")

    else:
        playlist_Data["playlist_Cover"] = urllib.request.urlopen(playlist_Data["images"][1]["url"]).read() #Скачивание обложки

        bot_Spotify_Sender.playlist_Ready(user_ID, playlist_Data, language_Name=language_Name)
        logger.info(f"Super Shuffle Created Successfuly For User {user_ID}")

    finally:
        to_Main_Menu(user_ID)