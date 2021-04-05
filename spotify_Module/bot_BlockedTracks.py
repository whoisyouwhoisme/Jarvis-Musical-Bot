import urllib
from spotify_Module import bot_Sender
from spotify_Module import localization
from spotify_Module import spotify_Service
from libraries import database_Manager as db_Manager
from spotify_Module import spotify_Exceptions
from spotify_Module.spotify_Logger import logger



def to_Main_Menu(user_ID):
    """
    Вернуть пользователя в главное меню
    """
    logger.info(f"Sending Main Menu Keyboard For User {user_ID}")
    db_Manager.write_User_Position(user_ID, "main_Menu")
    user_Language = db_Manager.get_User_Language(user_ID)
    bot_Sender.controls_Main_Menu(user_ID, language_Name=user_Language)



def in_Work(user_ID):
    """
    Поставить пользователю позицию in Work
    """
    logger.info(f"Sending In Work State For User {user_ID}")
    db_Manager.write_User_Position(user_ID, "work_In_Progress")
    user_Language = db_Manager.get_User_Language(user_ID)
    bot_Sender.downloading_Information(user_ID, language_Name=user_Language)



def send_BlockedTracks(user_ID, language_Name):
    try:
        in_Work(user_ID)
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)
        blocked_Data = spotify_Service.get_User_Blocked_Tracks(user_Unique_ID)

    except spotify_Exceptions.no_Tracks:
        bot_Sender.not_Enough_Songs(user_ID, language_Name=language_Name)

    except spotify_Exceptions.http_Error:
        bot_Sender.cannot_Authorize(user_ID, language_Name=language_Name)
        logger.error(f"HTTP ERROR OCCURED WHEN PREPARING BLOCKED TRACKS FOR USER {user_ID}")

    except spotify_Exceptions.http_Connection_Error:
        bot_Sender.servers_Link_Error(user_ID, language_Name=language_Name)
        logger.error(f"CONNECTION ERROR OCCURED WHEN PREPARING BLOCKED TRACKS FOR USER {user_ID}")

    except:
        bot_Sender.unknown_Error(user_ID, language_Name=language_Name)
        logger.error(f"UNKNOWN ERROR OCCURED WHEN PREPARING SUPER SHUFFLE FOR USER {user_ID}")        

    else:
        bot_Sender.blocked_Tracks(user_ID, blocked_Data=blocked_Data, language_Name=language_Name)

    finally:
        to_Main_Menu(user_ID)