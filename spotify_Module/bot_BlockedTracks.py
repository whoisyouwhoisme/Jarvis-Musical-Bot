from spotify_Module import bot_Sender
from spotify_Module import spotify_Service
from libraries import database_Manager as db_Manager
from spotify_Module import spotify_Exceptions
from spotify_Module.spotify_Logger import logger
import json
import math



def to_Main_Menu(user_ID):
    """
    Return user to main menu
    """
    logger.info(f"Sending Main Menu Keyboard For User {user_ID}")
    db_Manager.write_User_Position(user_ID, "main_Menu")
    user_Language = db_Manager.get_User_Language(user_ID)
    bot_Sender.controls_Main_Menu(user_ID, language_Name=user_Language)



def in_Work(user_ID):
    """
    Set the user to an in Work position
    """
    logger.info(f"Sending In Work State For User {user_ID}")
    db_Manager.write_User_Position(user_ID, "work_In_Progress")
    user_Language = db_Manager.get_User_Language(user_ID)
    bot_Sender.downloading_Information(user_ID, language_Name=user_Language)



def process_BlockedTracks_List(user_ID, list_Page):
    """
    Prepare data for a new Blocked Tracks page

    user_ID - Telegram user ID

    list_Page - List data page
    """
    database_Blocked_Tracks = db_Manager.search_In_Database(db_Manager.get_User_UniqueID(user_ID), "users_BlockedTracks", "user_Unique_ID")[0][1]
    blocked_Tracks = json.loads(database_Blocked_Tracks)
    max_Pages = math.ceil(len(blocked_Tracks["items"]) / 10) #Get the number of pages
    current_Page = {
        "current_Page":list_Page,
        "max_Pages":max_Pages,
        "user_Country":blocked_Tracks["user_Country"],
        "blocked_Count":blocked_Tracks["blocked_Count"],
        "tracks_Count":blocked_Tracks["tracks_Count"],
        "creation_Timestamp":blocked_Tracks["creation_Timestamp"],
        "comparsion_Timestamp":blocked_Tracks["comparsion_Timestamp"],
        "items":{},
    }

    start_Index = (10 * list_Page) - 10
    stop_Index = 10 * list_Page
    for item in range(start_Index, stop_Index):
        if item < len(blocked_Tracks["items"]):
            current_Page["items"][item] = {
                "prefix":blocked_Tracks["items"][item]["prefix"],
                "artists":blocked_Tracks["items"][item]["artists"],
                "name":blocked_Tracks["items"][item]["name"]
            }
    
    return current_Page



def send_BlockedTracks(user_ID, language_Name):
    try:
        in_Work(user_ID)
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)
        blocked_Data = spotify_Service.get_User_Blocked_Tracks(user_Unique_ID)
        logger.info(f"Get User Blocked Tracks For User {user_ID}")

    except spotify_Exceptions.no_Tracks:
        bot_Sender.not_Enough_Songs(user_ID, language_Name=language_Name)

    except spotify_Exceptions.http_Error:
        bot_Sender.cannot_Authorize(user_ID, language_Name=language_Name)
        logger.error(f"HTTP ERROR OCCURED WHEN PREPARING BLOCKED TRACKS FOR USER {user_ID}")

    except spotify_Exceptions.http_Connection_Error:
        bot_Sender.servers_Link_Error(user_ID, language_Name=language_Name)
        logger.error(f"CONNECTION ERROR OCCURED WHEN PREPARING BLOCKED TRACKS FOR USER {user_ID}")

    else:
        db_Manager.write_User_BlockedTracks(user_Unique_ID, blocked_Data=json.dumps(blocked_Data))

        try:
            bot_Sender.blocked_Tracks(user_ID, blocked_Data=process_BlockedTracks_List(user_ID, 1), language_Name=language_Name)
        
        except:
            bot_Sender.database_Error(user_ID, language_Name=language_Name)
            logger.error(f"DATABASE ERROR OCCURED WHEN PREPARING BLOCKED TRACKS LIST FOR USER {user_ID}")
        
        else:
            logger.info(f"Blocked Tracks List Prepared Successfuly For User {user_ID}")

    finally:
        to_Main_Menu(user_ID)