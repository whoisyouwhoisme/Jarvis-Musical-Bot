from libraries import database_Manager as db_Manager
from spotify_Module import spotify_Service
from spotify_Module import spotify_Exceptions
from spotify_Module import bot_Spotify_Sender
from spotify_Module.spotify_Logger import logger



def process_Inline_Data(data):
    user_ID = data.from_user.id
    inline_ID = data.id
    inline_Request = data.query.lower()

    if db_Manager.check_Spotify_Login(user_ID):
        user_Language = db_Manager.get_User_Language(user_ID)
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)

        if inline_Request == "share song":
            song_Sharing(user_ID=user_ID, inline_ID=inline_ID, user_Unique_ID=user_Unique_ID, user_Language=user_Language)
        
        if inline_Request == "share context":
            context_Sharing(user_ID=user_ID, inline_ID=inline_ID, user_Unique_ID=user_Unique_ID, user_Language=user_Language)

    else:
        bot_Spotify_Sender.inline_Spotify_Not_Authorized(inline_ID, language_Name=user_Language)



def song_Sharing(user_ID, inline_ID, user_Unique_ID, user_Language):
    try:
        user_Data = spotify_Service.get_Current_Playing(user_Unique_ID)

    except spotify_Exceptions.no_Data:
        bot_Spotify_Sender.inline_NowPlaying_Error(inline_ID, language_Name=user_Language)

    except spotify_Exceptions.no_Playback:
        bot_Spotify_Sender.inline_NowPlaying_Nothing(inline_ID, language_Name=user_Language)

    except spotify_Exceptions.private_Session_Enabled:
        bot_Spotify_Sender.inline_Private_Session(inline_ID, language_Name=user_Language)

    except spotify_Exceptions.http_Error:
        bot_Spotify_Sender.inline_Auth_Error(inline_ID, language_Name=user_Language)
        logger.error(f"INLINE MODE ERROR. OAUTH ERROR WHEN SENDING NOW PLAYING FOR USER {user_ID}")

    except:
        bot_Spotify_Sender.inline_Unknown_Error(inline_ID, language_Name=user_Language)
        logger.error(f"INLINE MODE ERROR. UNKNOWN ERROR WHEN SENDING NOW PLAYING FOR USER {user_ID}")
    
    else:
        bot_Spotify_Sender.share_Inline_NowPlaying(inline_ID, user_Data, language_Name=user_Language)



def context_Sharing(user_ID, inline_ID, user_Unique_ID, user_Language):
    try:
        current_Context = spotify_Service.get_Current_Context(user_Unique_ID)
        context = current_Context["context_URI"].split(":")
        context_ID = context[-1] #Обычно ID контекста находится в самом конце

        if current_Context["context_Type"] == "album":
            context_Data = spotify_Service.get_Album_Data(user_Unique_ID, context_ID)

        elif current_Context["context_Type"] == "artist":
            context_Data = spotify_Service.get_Artist_Data(user_Unique_ID, context_ID)

        elif current_Context["context_Type"] == "playlist":
            context_Data = spotify_Service.get_Playlist_Data(user_Unique_ID, context_ID)
    
    except spotify_Exceptions.no_Playback:
        bot_Spotify_Sender.inline_NowPlaying_Nothing(inline_ID, language_Name=user_Language)
    
    except spotify_Exceptions.no_Playing_Context:
        bot_Spotify_Sender.inline_No_Context(inline_ID, language_Name=user_Language)

    except spotify_Exceptions.private_Session_Enabled:
        bot_Spotify_Sender.inline_Private_Session(inline_ID, language_Name=user_Language)

    except spotify_Exceptions.http_Error:
        bot_Spotify_Sender.inline_Auth_Error(inline_ID, language_Name=user_Language)
        logger.error(f"INLINE MODE ERROR. OAUTH ERROR WHEN SENDING NOW PLAYING FOR USER {user_ID}")

    except:
        bot_Spotify_Sender.inline_Unknown_Error(inline_ID, language_Name=user_Language)
        logger.error(f"INLINE MODE ERROR. UNKNOWN ERROR WHEN SENDING NOW PLAYING FOR USER {user_ID}")
    
    else:
        if current_Context["context_Type"] == "album":
            bot_Spotify_Sender.share_Inline_Album(inline_ID, context_Data, language_Name=user_Language)

        elif current_Context["context_Type"] == "artist":
            bot_Spotify_Sender.share_Inline_Artist(inline_ID, context_Data, language_Name=user_Language)

        elif current_Context["context_Type"] == "playlist":
            bot_Spotify_Sender.share_Inline_Playlist(inline_ID, context_Data, language_Name=user_Language)