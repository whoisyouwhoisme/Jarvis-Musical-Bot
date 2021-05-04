import urllib
import json
import math
from spotify_Module import localization
from spotify_Module import bot_Sender
from spotify_Module import spotify_Service
from libraries import database_Manager as db_Manager
from spotify_Module import spotify_Exceptions
from spotify_Module.spotify_Logger import logger
from collections import Counter



language_Vocabluary = localization.load_Vocabluary()



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



def process_Type_Selector_Message(user_ID, message_Text, user_Language):
    """
    Keyboard messages handler
    """
    if message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["by_Decades"]:
        in_Work(user_ID)
        create_Decades_Statistic(user_ID, language_Name=user_Language)

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["by_Artists"]:
        in_Work(user_ID)
        create_Artists_Statistic(user_ID, language_Name=user_Language)

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["by_Genres"]:
        in_Work(user_ID)
        create_Genres_Statistic(user_ID, language_Name=user_Language)       

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"]:
        to_Main_Menu(user_ID)

    else:
        bot_Sender.astray_Notification(user_ID, language_Name=user_Language)



def create_Decades_Statistic(user_ID, language_Name):
    """
    Sends statistics for decades
    """
    try:
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)
        saved_Tracks = spotify_Service.get_Saved_Raw_Tracks(user_Unique_ID)
        total_Tracks = len(saved_Tracks)

        tracks_Decades = []
        for item in range(len(saved_Tracks)):
            release_Date = saved_Tracks[item]["track"]["album"]["release_date"]
            track_Year = release_Date.split("-")[0] #The year always comes first
            track_Decade = int(int(track_Year) / 10) * 10 #Calculating a decade

            tracks_Decades.append(track_Decade)
        
        decades_Count = Counter(tracks_Decades)
        decades_Most_Common = decades_Count.most_common(10)

        most_Popular_Decades = {"total_Tracks":total_Tracks, "statistic_Data":[]}
        for decade in range(len(decades_Most_Common)):
            percent_Of_Total = round(((decades_Most_Common[decade][1] / total_Tracks) * 100), 1)

            most_Popular_Decades["statistic_Data"].append({
                "decade":decades_Most_Common[decade][0],
                "tracks_In_Decade":decades_Most_Common[decade][1],
                "percent_Of_Total":percent_Of_Total
            })
    
    except spotify_Exceptions.no_Tracks:
        bot_Sender.not_Enough_Songs(user_ID, language_Name=language_Name)

    except spotify_Exceptions.http_Error:
        bot_Sender.cannot_Authorize(user_ID, language_Name=language_Name)
        logger.error(f"HTTP ERROR OCCURED WHEN PREPARING DECADES STATISTIC FOR USER {user_ID}")

    except spotify_Exceptions.http_Connection_Error:
        bot_Sender.servers_Link_Error(user_ID, language_Name=language_Name)
        logger.error(f"CONNECTION ERROR OCCURED WHEN PREPARING DECADES STATISTIC FOR USER {user_ID}")

    except:
        bot_Sender.unknown_Error(user_ID, language_Name=language_Name)
        logger.error(f"UNKNOWN ERROR OCCURED WHEN PREPARING DECADES STATISTIC FOR USER {user_ID}")

    else:
        bot_Sender.decades_Statistic(user_ID, statistic_Data=most_Popular_Decades, language_Name=language_Name)
        logger.info(f"Decades Statistic Created Successfuly For User {user_ID}")

    finally:
        to_Main_Menu(user_ID)



def create_Artists_Statistic(user_ID, language_Name):
    """
    Sends statistics on performers
    """
    try:
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)
        saved_Tracks = spotify_Service.get_Saved_Raw_Tracks(user_Unique_ID)
        total_Tracks = len(saved_Tracks)

        tracks_Artists = []
        for item in range(len(saved_Tracks)):
            track_Artist = saved_Tracks[item]["track"]["album"]["artists"][0]["name"]

            tracks_Artists.append(track_Artist)
        
        artists_Count = Counter(tracks_Artists)
        artists_Most_Common = artists_Count.most_common(15)

        most_Popular_Artists = {"total_Tracks":total_Tracks, "statistic_Data":[]}
        for artist in range(len(artists_Most_Common)):
            percent_Of_Total = round(((artists_Most_Common[artist][1] / total_Tracks) * 100), 1)

            most_Popular_Artists["statistic_Data"].append({
                "artist":artists_Most_Common[artist][0],
                "artist_Tracks":artists_Most_Common[artist][1],
                "percent_Of_Total":percent_Of_Total
            })

    except spotify_Exceptions.no_Tracks:
        bot_Sender.not_Enough_Songs(user_ID, language_Name=language_Name)

    except spotify_Exceptions.http_Error:
        bot_Sender.cannot_Authorize(user_ID, language_Name=language_Name)
        logger.error(f"HTTP ERROR OCCURED WHEN PREPARING ARTISTS STATISTIC FOR USER {user_ID}")

    except spotify_Exceptions.http_Connection_Error:
        bot_Sender.servers_Link_Error(user_ID, language_Name=language_Name)
        logger.error(f"CONNECTION ERROR OCCURED WHEN PREPARING ARTISTS STATISTIC FOR USER {user_ID}")

    except:
        bot_Sender.unknown_Error(user_ID, language_Name=language_Name)
        logger.error(f"UNKNOWN ERROR OCCURED WHEN PREPARING ARTISTS STATISTIC FOR USER {user_ID}")

    else:
        bot_Sender.artists_Statistic(user_ID, statistic_Data=most_Popular_Artists, language_Name=language_Name)
        logger.info(f"Artists Statistic Created Successfuly For User {user_ID}")

    finally:
        to_Main_Menu(user_ID)



def create_Genres_Statistic(user_ID, language_Name):
    """
    Sends statistics by genre
    """
    try:
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)
        saved_Tracks = spotify_Service.get_Saved_Raw_Tracks(user_Unique_ID)

        artists_Uris = []
        for item in range(len(saved_Tracks)):
            artist_Uri = saved_Tracks[item]["track"]["album"]["artists"][0]["uri"][15:]

            artists_Uris.append(artist_Uri)

        total_Iterations = math.ceil(len(saved_Tracks) / 50) #Divide the number of artists into requests by 50 artists

        offset = 50
        genres = []
        for _ in range(total_Iterations): #Get all artists
            artists_Data = spotify_Service.get_Several_Artists(user_Unique_ID, artists_Uris[offset - 50:offset])

            offset += 50
            
            for artist in range(len(artists_Data["artists"])):
                genres += artists_Data["artists"][artist]["genres"]
        
        genres_Count = Counter(genres)
        genres_Most_Common = genres_Count.most_common(10)

        most_Popular_Genres = []
        for genre in range(len(genres_Most_Common)):
            most_Popular_Genres.append(genres_Most_Common[genre][0])

    except spotify_Exceptions.no_Tracks:
        bot_Sender.not_Enough_Songs(user_ID, language_Name=language_Name)

    except spotify_Exceptions.http_Error:
        bot_Sender.cannot_Authorize(user_ID, language_Name=language_Name)
        logger.error(f"HTTP ERROR OCCURED WHEN PREPARING GENRES STATISTIC FOR USER {user_ID}")

    except spotify_Exceptions.http_Connection_Error:
        bot_Sender.servers_Link_Error(user_ID, language_Name=language_Name)
        logger.error(f"CONNECTION ERROR OCCURED WHEN PREPARING GENRES STATISTIC FOR USER {user_ID}")

    except:
        bot_Sender.unknown_Error(user_ID, language_Name=language_Name)
        logger.error(f"UNKNOWN ERROR OCCURED WHEN PREPARING GENRES STATISTIC FOR USER {user_ID}")

    else:
        bot_Sender.genres_Statistic(user_ID, statistic_Data=most_Popular_Genres, language_Name=language_Name)
        logger.info(f"Genres Statistic Created Successfuly For User {user_ID}")

    finally:
        to_Main_Menu(user_ID)