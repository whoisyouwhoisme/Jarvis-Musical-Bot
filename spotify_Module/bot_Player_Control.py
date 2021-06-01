from libraries import database_Manager as db_Manager
from spotify_Module import spotify_Service
from spotify_Module import spotify_Exceptions
from spotify_Module import bot_Sender
from spotify_Module.spotify_Logger import logger



def start_Playback(playback_Type, playback_URI, user_ID, user_Language):
    try:
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)

        if playback_Type == "album":
            playlist_ID = "spotify:album:" + playback_URI
            spotify_Service.start_Playback(user_Unique_ID, playback_Context=playlist_ID)

        elif playback_Type == "artist":
            playlist_ID = "spotify:artist:" + playback_URI
            spotify_Service.start_Playback(user_Unique_ID, playback_Context=playlist_ID)

        elif playback_Type == "playlist":
            playlist_ID = "spotify:playlist:" + playback_URI
            spotify_Service.start_Playback(user_Unique_ID, playback_Context=playlist_ID)

        elif playback_Type == "track":
            track_ID = "spotify:track:" + playback_URI
            spotify_Service.add_Track_To_Queue(user_Unique_ID, track_Uri=track_ID)

    except spotify_Exceptions.no_ActiveDevices:
        bot_Sender.no_ActiveDevices(user_ID, user_Language)

    except spotify_Exceptions.premium_Required:
        bot_Sender.premium_Required(user_ID, language_Name=user_Language)

    except spotify_Exceptions.playback_Error:
        bot_Sender.playback_Error(user_ID, language_Name=user_Language)
    
    except spotify_Exceptions.http_Error:
        bot_Sender.cannot_Authorize(user_ID, language_Name=user_Language)

    except:
        bot_Sender.unknown_Error(user_ID, language_Name=user_Language)
    
    else:
        if playback_Type == "album" or playback_Type == "artist" or playback_Type == "playlist":
            bot_Sender.playback_Started(user_ID, language_Name=user_Language)
        
        elif playback_Type == "track":
            try:
                track_Info = spotify_Service.get_Track_Info(user_Unique_ID, track_URI=playback_URI)
            
            except:
                bot_Sender.song_Added_To_Queue(user_ID, language_Name=user_Language)
                logger.error(f"CANNOT GET DETAILED TRACK INFO {playback_URI} FOR USER {user_ID}")
            
            else:
                bot_Sender.song_Added_To_Queue(user_ID, track_Info=track_Info, language_Name=user_Language)