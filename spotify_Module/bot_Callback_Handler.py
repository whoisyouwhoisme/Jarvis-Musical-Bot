from libraries import database_Manager as db_Manager
from spotify_Module import bot_Sender
from spotify_Module import bot_LibraryTops
from spotify_Module import bot_Player_Control
from spotify_Module import bot_BlockedTracks
from spotify_Module.spotify_Logger import logger



def process_Callback_Data(data):
    user_ID = data.from_user.id
    logger.info(f"New Callback Data: {data.data} From: {user_ID}")

    if db_Manager.check_Spotify_Login(user_ID):
        user_Language = db_Manager.get_User_Language(user_ID)
        callback_Request = data.data.split("#")

        if callback_Request[0] == "player": #If the message from the player section
            if callback_Request[1] == "play":
                bot_Player_Control.start_Playback(callback_Request[2], callback_Request[3], user_ID=user_ID, user_Language=user_Language)
        
        if data.message: #For some reason, messages sent from Inline do not have a message body
            message_ID = data.message.message_id

            if callback_Request[0] == "interface": #If the message from the interface section
                if callback_Request[1] == "topTracks":
                    if callback_Request[2] == "createPlaylist":
                            bot_LibraryTops.create_TopTracks_Playlist(user_ID, language_Name=user_Language, time_Range=callback_Request[3])
                    
                    elif callback_Request[2] == "page":
                        page_Number = int(callback_Request[4])
                        top_Data = bot_LibraryTops.process_TopTracks_List(user_ID, time_Range=callback_Request[3], list_Page=page_Number)
                        bot_Sender.tracks_Top(user_ID, top_Data, language_Name=user_Language, message_ID=message_ID)
                
                elif callback_Request[1] == "topArtists":
                    if callback_Request[2] == "page":
                        page_Number = int(callback_Request[4])
                        top_Data = bot_LibraryTops.process_TopArtists_List(user_ID, time_Range=callback_Request[3], list_Page=page_Number)
                        bot_Sender.artists_Top(user_ID, top_Data, language_Name=user_Language, message_ID=message_ID)
                
                elif callback_Request[1] == "blockedTracks":
                    if callback_Request[2] == "page":
                        page_Number = int(callback_Request[3])
                        blocked_Data = bot_BlockedTracks.process_BlockedTracks_List(user_ID, list_Page=page_Number)
                        bot_Sender.blocked_Tracks(user_ID, blocked_Data=blocked_Data, language_Name=user_Language, message_ID=message_ID)