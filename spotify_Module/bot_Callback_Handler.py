from libraries import database_Manager as db_Manager
from spotify_Module import spotify_Service
from spotify_Module import spotify_Exceptions
from spotify_Module import bot_Spotify_Sender
from spotify_Module import bot_LibraryTops
from spotify_Module.spotify_Logger import logger


def process_Callback_Data(data):
    user_ID = data.from_user.id
    logger.info(f"New Callback Data: {data.data} From: {user_ID}")

    if db_Manager.check_Spotify_Login(user_ID):
        user_Language = db_Manager.get_User_Language(user_ID) #Записать в переменную язык пользователя
        callback_Request = data.data.split("#") #Парсим строку

        if callback_Request[0] == "player": #Если сообщение из раздела плеера
            if callback_Request[1] == "play":
                try:
                    if callback_Request[2] == "album":
                        playlist_ID = "spotify:album:" + callback_Request[3]
                        spotify_Service.start_Playback(db_Manager.get_User_UniqueID(user_ID), playback_Context=playlist_ID)

                    elif callback_Request[2] == "artist":
                        playlist_ID = "spotify:artist:" + callback_Request[3]
                        spotify_Service.start_Playback(db_Manager.get_User_UniqueID(user_ID), playback_Context=playlist_ID)

                    elif callback_Request[2] == "playlist":
                        playlist_ID = "spotify:playlist:" + callback_Request[3]
                        spotify_Service.start_Playback(db_Manager.get_User_UniqueID(user_ID), playback_Context=playlist_ID)

                    elif callback_Request[2] == "track":
                        track_ID = "spotify:track:" + callback_Request[3]
                        spotify_Service.add_Track_To_Queue(db_Manager.get_User_UniqueID(user_ID), track_Uri=track_ID)

                except spotify_Exceptions.no_ActiveDevices:
                    bot_Spotify_Sender.no_ActiveDevices(user_ID, user_Language)

                except spotify_Exceptions.premium_Required:
                    bot_Spotify_Sender.premium_Required(user_ID, language_Name=user_Language)

                except spotify_Exceptions.playback_Error:
                    bot_Spotify_Sender.playback_Error(user_ID, language_Name=user_Language)
                
                except spotify_Exceptions.http_Error:
                    bot_Spotify_Sender.cannot_Authorize(user_ID, language_Name=user_Language)

                except:
                    bot_Spotify_Sender.unknown_Error(user_ID, language_Name=user_Language)
                
                else:
                    if callback_Request[2] == "album" or callback_Request[2] == "artist" or callback_Request[2] == "playlist":
                        bot_Spotify_Sender.playback_Started(user_ID, language_Name=user_Language)
                    
                    elif callback_Request[2] == "track":
                        bot_Spotify_Sender.song_Added_To_Queue(user_ID, language_Name=user_Language)
        
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