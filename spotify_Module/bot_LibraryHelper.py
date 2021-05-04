from spotify_Module import localization
from spotify_Module import bot_Sender
from libraries import database_Manager as db_Manager
from spotify_Module import spotify_Exceptions
from spotify_Module.spotify_Logger import logger
from spotify_Module import spotify_Service
from collections import Counter



language_Vocabluary = localization.load_Vocabluary()



duplicate_User_Playlist_Songs = {}
duplicate_User_Liked_Songs = {}



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



def removing_Work(user_ID):
    """
    Set the user to an in Work position
    """    
    logger.info(f"Sending In Work State For User {user_ID}")
    db_Manager.write_User_Position(user_ID, "work_In_Progress")
    user_Language = db_Manager.get_User_Language(user_ID)
    bot_Sender.removing_In_Progress(user_ID, language_Name=user_Language)



def process_Type_Selector_Message(user_ID, message_Text, user_Language):
    """
    Keyboard messages handler
    """
    if message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["library_Duplicates"]:
        bot_Sender.duplicates_Remover_Description(user_ID, section_Name="liked_Songs", language_Name=user_Language)
        in_Work(user_ID)
        analyze_Liked_Tracks(user_ID, user_Language=user_Language)

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["playlist_Duplicates"]:
        bot_Sender.duplicates_Remover_Description(user_ID, section_Name="playlist", language_Name=user_Language)
        in_Work(user_ID)
        get_Available_Playlists(user_ID, language_Name=user_Language)
        db_Manager.write_User_Position(user_ID, "user_PlaylistDuplicates_SelectPlaylist")

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"]:
        to_Main_Menu(user_ID)

    else:
        bot_Sender.astray_Notification(user_ID, language_Name=user_Language)



def process_Removing_Choice(user_ID, message_Text, tracks_Section, user_Language):
    """
    Delete action selection processing

    tracks_Section - playlist OR likedSongs
    """
    if message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["delete"]:
        removing_Work(user_ID)
        delete_Tracks(user_ID, tracks_Section=tracks_Section, user_Language=user_Language)

    elif message_Text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["leave_As_Is"]:
        to_Main_Menu(user_ID)

    else:
        bot_Sender.astray_Notification(user_ID, language_Name=user_Language)



def delete_Tracks(user_ID, tracks_Section, user_Language):
    """
    Removes tracks from tracks_Section

    tracks_Section - playlist OR likedSongs
    """
    user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)

    user_Library = {}
    if tracks_Section == "playlist":
        user_Library = duplicate_User_Playlist_Songs[user_ID]
    elif tracks_Section == "likedSongs":
        user_Library = duplicate_User_Liked_Songs[user_ID]

    print(user_Library["tracks"])

    tracks_To_Delete = []
    for track_Item in range(len(user_Library["tracks"])):
        for _ in range(user_Library["tracks"][track_Item]["duplicate_Count"] - 1):
            tracks_To_Delete.append(user_Library["tracks"][track_Item]["uri"])
    
    print(tracks_To_Delete)

    if tracks_Section == "playlist":
        success = spotify_Service.delete_Playlist_Tracks(user_Unique_ID, playlist_Uri=user_Library["playlist_Uri"], tracks_To_Delete=tracks_To_Delete)
    elif tracks_Section == "likedSongs":
        success = spotify_Service.delete_Liked_Tracks(user_Unique_ID, tracks_To_Delete=tracks_To_Delete)

    if success:
        bot_Sender.removing_Success(user_ID, language_Name=user_Language)
        to_Main_Menu(user_ID)
    
    else:
        bot_Sender.removing_Failure(user_ID, language_Name=user_Language)
        to_Main_Menu(user_ID)



def analyze_Liked_Tracks(user_ID, user_Language):
    """
    Analyze favorite tracks for duplicates
    """
    try:
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)

        user_Liked_Tracks = spotify_Service.download_User_LikedSongs(user_Unique_ID)

        liked_Tracks_Uris = []
        for track in range(len(user_Liked_Tracks)):
            liked_Tracks_Uris.append(user_Liked_Tracks[track]["uri"])
        
        duplicate_Tracks = []
        for item, count in Counter(liked_Tracks_Uris).items():
            if count > 1:
                duplicate_Tracks.append({
                    "uri":item,
                    "count":count
                })
        
        duplicate_Tracks_Info = {"tracks":[]}
        for duplicate_Track in range(len(duplicate_Tracks)):
            for track in range(len(user_Liked_Tracks)):
                if duplicate_Tracks[duplicate_Track]["uri"] == user_Liked_Tracks[track]["uri"]:
                    duplicate_Tracks_Info["tracks"].append({
                        "name":user_Liked_Tracks[track]["name"],
                        "artists":user_Liked_Tracks[track]["artists"],
                        "uri":user_Liked_Tracks[track]["uri"],
                        "duplicate_Count":duplicate_Tracks[duplicate_Track]["count"]
                    })
                    break

    except spotify_Exceptions.http_Error:
        bot_Sender.cannot_Authorize(user_ID, language_Name=user_Language)
        logger.error(f"HTTP ERROR OCCURED WHEN ANALYZING LIKED SONGS FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    except spotify_Exceptions.http_Connection_Error:
        bot_Sender.servers_Link_Error(user_ID, language_Name=user_Language)
        logger.error(f"CONNECTION ERROR OCCURED WHEN ANALYZING LIKED SONGS FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    except:
        bot_Sender.unknown_Error(user_ID, language_Name=user_Language)
        logger.error(f"UNKNOWN ERROR OCCURED WHEN ANALYZING LIKED SONGS FOR USER {user_ID}")
        to_Main_Menu(user_ID)
    
    else:
        if len(duplicate_Tracks_Info["tracks"]) == 0:
            bot_Sender.duplicates_Not_Found(user_ID, language_Name=user_Language)
            to_Main_Menu(user_ID)

        else:
            #db_Manager.write_User_Position(user_ID, "user_LikedSongsDuplicates_MakeChoice")
            #duplicate_User_Liked_Songs[user_ID] = duplicate_Tracks_Info
            bot_Sender.duplicates_Found(user_ID, duplicates_Data=duplicate_Tracks_Info, language_Name=user_Language)
            to_Main_Menu(user_ID)






def analyze_Playlist(user_ID, user_Language, playlist_Name):
    """
    Analyze playlist for duplicates
    """
    try:
        in_Work(user_ID)
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)
        playlists = spotify_Service.get_User_Playlists(user_Unique_ID)

        selected_Playlist_Uri = None
        for playlist in range(len(playlists)):
            if playlists[playlist]["playlist_Name"] == playlist_Name:
                selected_Playlist_Uri = playlists[playlist]["playlist_Uri"]
                break
        
        if not selected_Playlist_Uri:
            raise spotify_Exceptions.playlist_Not_Found
        
        else:
            playlist_Tracks = spotify_Service.get_Playlist_Tracks(user_Unique_ID, selected_Playlist_Uri[17:])

            playlist_Tracks_Uris = []
            for track in range(len(playlist_Tracks)):
                playlist_Tracks_Uris.append(playlist_Tracks[track]["uri"])    

            duplicate_Tracks = []
            for item, count in Counter(playlist_Tracks_Uris).items():
                if count > 1:
                    duplicate_Tracks.append({
                        "uri":item,
                        "count":count
                    })
            
            duplicate_Tracks_Info = {"playlist_Uri":selected_Playlist_Uri[17:],"tracks":[]}
            for duplicate_Track in range(len(duplicate_Tracks)):
                for track in range(len(playlist_Tracks)):
                    if duplicate_Tracks[duplicate_Track]["uri"] == playlist_Tracks[track]["uri"]:
                        duplicate_Tracks_Info["tracks"].append({
                            "name":playlist_Tracks[track]["name"],
                            "artists":playlist_Tracks[track]["artists"],
                            "uri":playlist_Tracks[track]["uri"],
                            "duplicate_Count":duplicate_Tracks[duplicate_Track]["count"]
                        })
                        break
    
    except spotify_Exceptions.playlist_Not_Found:
        bot_Sender.playlist_NotFound(user_ID, language_Name=user_Language)
        to_Main_Menu(user_ID)

    except spotify_Exceptions.http_Error:
        bot_Sender.cannot_Authorize(user_ID, language_Name=user_Language)
        logger.error(f"HTTP ERROR OCCURED WHEN ANALYZING PLAYLIST FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    except spotify_Exceptions.http_Connection_Error:
        bot_Sender.servers_Link_Error(user_ID, language_Name=user_Language)
        logger.error(f"CONNECTION ERROR OCCURED WHEN ANALYZING PLAYLIST FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    except:
        bot_Sender.unknown_Error(user_ID, language_Name=user_Language)
        logger.error(f"UNKNOWN ERROR OCCURED WHEN ANALYZING PLAYLIST FOR USER {user_ID}")
        to_Main_Menu(user_ID)
    
    else:
        if len(duplicate_Tracks_Info["tracks"]) == 0:
            bot_Sender.duplicates_Not_Found(user_ID, language_Name=user_Language)
            to_Main_Menu(user_ID)

        else:
            #db_Manager.write_User_Position(user_ID, "user_PlaylistDuplicates_MakeChoice")
            #duplicate_User_Playlist_Songs[user_ID] = duplicate_Tracks_Info
            bot_Sender.duplicates_Found(user_ID, duplicates_Data=duplicate_Tracks_Info, language_Name=user_Language)
            to_Main_Menu(user_ID)



def get_Available_Playlists(user_ID, language_Name):
    """
    Get playlists available to a user
    """
    try:
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)
        playlists = spotify_Service.get_User_Playlists(user_Unique_ID)

    except spotify_Exceptions.no_Playlists:
        bot_Sender.no_Playlists(user_ID, language_Name=language_Name)
        to_Main_Menu(user_ID)

    except spotify_Exceptions.http_Error:
        bot_Sender.cannot_Authorize(user_ID, language_Name=language_Name)
        logger.error(f"HTTP ERROR OCCURED WHEN PREPARING AVAILABLE PLAYLISTS FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    except spotify_Exceptions.http_Connection_Error:
        bot_Sender.servers_Link_Error(user_ID, language_Name=language_Name)
        logger.error(f"CONNECTION ERROR OCCURED WHEN PREPARING AVAILABLE PLAYLISTS FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    except:
        bot_Sender.unknown_Error(user_ID, language_Name=language_Name)
        logger.error(f"UNKNOWN ERROR OCCURED WHEN PREPARING AVAILABLE PLAYLISTS FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    else:
        bot_Sender.send_Playlist_Selector(user_ID, playlists_Names=playlists, language_Name=language_Name)
        logger.info(f"Playlists List Successfully Loaded For User {user_ID}")