from libraries import database_Manager as db_Manager
from spotify_Module import spotify_Service
from spotify_Module import spotify_Exceptions
from spotify_Module import bot_Inline_Sender
from spotify_Module.spotify_Logger import logger



def process_User_Language(language_Code):
    if language_Code == "ru" or language_Code == "uk" or language_Code == "be": #Russian, Ukrainian, Belarusian
        user_Language = "RUS"
    else:
        user_Language = "ENG"
    
    return user_Language



def process_Inline_Data(data):
    user_ID = data.from_user.id
    inline_ID = data.id
    inline_Request = data.query.lower()

    if db_Manager.check_Spotify_Login(user_ID):
        user_Language = db_Manager.get_User_Language(user_ID)
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)

        if inline_Request == "share":
            logger.info(f"Song Sharing For User {user_ID}")
            song_Sharing(user_ID, inline_ID, user_Unique_ID, user_Language)
        
        if inline_Request == "share context":
            logger.info(f"Context Sharing For User {user_ID}")
            context_Sharing(user_ID, inline_ID, user_Unique_ID, user_Language)
        
        if inline_Request[:6] == "search":
            if len(inline_Request[7:]) > 0:
                logger.info(f"Song Searching For User {user_ID}")
                search_Request = inline_Request[7:]
                items_Search(user_ID, inline_ID, search_Request, user_Unique_ID, user_Language)
    else:
        bot_Inline_Sender.inline_Spotify_Not_Authorized(inline_ID, process_User_Language(data.from_user.language_code))



def song_Sharing(user_ID, inline_ID, user_Unique_ID, user_Language):
    try:
        user_Data = spotify_Service.get_Current_Playing(user_Unique_ID)

    except spotify_Exceptions.no_Data:
        bot_Inline_Sender.inline_NowPlaying_Error(inline_ID, user_Language)

    except spotify_Exceptions.no_Playback:
        bot_Inline_Sender.inline_NowPlaying_Nothing(inline_ID, user_Language)
    
    except spotify_Exceptions.local_Playing:
        bot_Inline_Sender.cannot_Share_Local_Playing(inline_ID, user_Language)

    except spotify_Exceptions.private_Session_Enabled:
        bot_Inline_Sender.inline_Private_Session(inline_ID, user_Language)

    except spotify_Exceptions.http_Error:
        logger.error(f"INLINE MODE ERROR. OAUTH ERROR WHEN SENDING NOW PLAYING FOR USER {user_ID}")
        bot_Inline_Sender.inline_Auth_Error(inline_ID, user_Language)

    except:
        logger.error(f"INLINE MODE ERROR. UNKNOWN ERROR WHEN SENDING NOW PLAYING FOR USER {user_ID}")
        bot_Inline_Sender.inline_Unknown_Error(inline_ID, user_Language)
    
    else:
        bot_Inline_Sender.share_Inline_NowPlaying(inline_ID, user_Data, user_Language)



def context_Sharing(user_ID, inline_ID, user_Unique_ID, user_Language):
    try:
        current_Context = spotify_Service.get_Current_Context(user_Unique_ID)
        context = current_Context["context_URI"].split(":")
        context_ID = context[-1] #Usually the context ID is at the very end

        if current_Context["context_Type"] == "album":
            context_Data = spotify_Service.get_Album_Data(user_Unique_ID, context_ID)

        elif current_Context["context_Type"] == "artist":
            context_Data = spotify_Service.get_Artist_Data(user_Unique_ID, context_ID)

        elif current_Context["context_Type"] == "playlist":
            context_Data = spotify_Service.get_Playlist_Data(user_Unique_ID, context_ID)
    
    except spotify_Exceptions.no_Playback:
        bot_Inline_Sender.inline_NowPlaying_Nothing(inline_ID, user_Language)
    
    except spotify_Exceptions.no_Playing_Context:
        bot_Inline_Sender.inline_No_Context(inline_ID, user_Language)

    except spotify_Exceptions.private_Session_Enabled:
        bot_Inline_Sender.inline_Private_Session(inline_ID, user_Language)

    except spotify_Exceptions.http_Error:
        logger.error(f"INLINE MODE ERROR. OAUTH ERROR WHEN SENDING NOW PLAYING FOR USER {user_ID}")
        bot_Inline_Sender.inline_Auth_Error(inline_ID, user_Language)

    except:
        logger.error(f"INLINE MODE ERROR. UNKNOWN ERROR WHEN SENDING NOW PLAYING FOR USER {user_ID}")
        bot_Inline_Sender.inline_Unknown_Error(inline_ID, user_Language)
    
    else:
        if current_Context["context_Type"] == "album":
            bot_Inline_Sender.share_Inline_Album(inline_ID, context_Data, user_Language)

        elif current_Context["context_Type"] == "artist":
            bot_Inline_Sender.share_Inline_Artist(inline_ID, context_Data, user_Language)

        elif current_Context["context_Type"] == "playlist":
            bot_Inline_Sender.share_Inline_Playlist(inline_ID, context_Data, user_Language)



def items_Search(user_ID, inline_ID, search_Request, user_Unique_ID, user_Language):
    try:
        search_Results = spotify_Service.search_Item(user_Unique_ID, search_Request, limit=10)

    except spotify_Exceptions.search_No_Results:
        bot_Inline_Sender.search_No_Results(inline_ID, user_Language)
        
    except spotify_Exceptions.http_Error:
        logger.error(f"INLINE MODE ERROR. OAUTH ERROR WHEN SENDING NOW PLAYING FOR USER {user_ID}")
        bot_Inline_Sender.inline_Auth_Error(inline_ID, user_Language)

    except:
        logger.error(f"INLINE MODE ERROR. UNKNOWN ERROR WHEN SENDING NOW PLAYING FOR USER {user_ID}")
        bot_Inline_Sender.inline_Unknown_Error(inline_ID, user_Language)
    
    else:
        bot_Inline_Sender.search_Results(inline_ID, search_Results, user_Language)