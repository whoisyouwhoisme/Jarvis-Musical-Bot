from libraries import database_Manager as db_Manager
from spotify_Module import spotify_Service
from spotify_Module import spotify_Exceptions
from spotify_Module import bot_Spotify_Sender
from spotify_Module import bot_LibraryTops
from spotify_Module import bot_Player_Control
from spotify_Module.spotify_Logger import logger



def process_Callback_Data(data):
    user_ID = data.from_user.id
    logger.info(f"New Callback Data: {data.data} From: {user_ID}")

    if db_Manager.check_Spotify_Login(user_ID):
        user_Language = db_Manager.get_User_Language(user_ID) #Записать в переменную язык пользователя
        callback_Request = data.data.split("#") #Парсим строку

        if callback_Request[0] == "player": #Если сообщение из раздела плеера
            if callback_Request[1] == "play":
                bot_Player_Control.start_Playback(callback_Request[2], callback_Request[3], user_ID=user_ID, user_Language=user_Language)
        
        if data.message: #По каким-то причинам у сообщений отправленных из Inline нету тела сообщения
            message_ID = data.message.message_id

            if callback_Request[0] == "interface": #Если сообщение из раздела интерфейса
                if callback_Request[1] == "topTracks":
                    if callback_Request[2] == "createPlaylist":
                            bot_LibraryTops.create_TopTracks_Playlist(user_ID, language_Name=user_Language, time_Range=callback_Request[3])
                    
                    elif callback_Request[2] == "page":
                        page_Number = int(callback_Request[4])
                        top_Data = bot_LibraryTops.process_TopTracks_List(user_ID, time_Range=callback_Request[3], list_Page=page_Number)
                        bot_Spotify_Sender.tracks_Top(user_ID, top_Data, language_Name=user_Language, message_ID=message_ID)
                
                elif callback_Request[1] == "topArtists":
                    if callback_Request[2] == "page":
                        page_Number = int(callback_Request[4])
                        top_Data = bot_LibraryTops.process_TopArtists_List(user_ID, time_Range=callback_Request[3], list_Page=page_Number)
                        bot_Spotify_Sender.artists_Top(user_ID, top_Data, language_Name=user_Language, message_ID=message_ID)