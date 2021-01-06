"""
Ребята не стоит вскрывать этот код. 
Вы молодые, шутливые, вам все легко. Это не то. Это не Stuxnet и даже не шпионские программы ЦРУ. Сюда лучше не лезть. 
Серьезно, любой из вас будет жалеть. 
Лучше закройте код и забудьте что там писалось. 
Я вполне понимаю что данным сообщением вызову дополнительный интерес, но хочу сразу предостеречь пытливых - стоп. Остальные просто не найдут.
"""

import time
import json
import math
import random
import urllib
from spotify_Module import localization
from spotify_Module import bot_Spotify_Sender
from spotify_Module import spotify_Service
from spotify_Module import spotify_Exceptions
from spotify_Module.spotify_Logger import logger
from libraries import spotify_Oauth
from libraries import database_Manager as db_Manager

bot_Version = 0.2

language_Vocabluary = localization.load_Vocabluary()

musicQuiz_User_Songs = {}
musicQuiz_User_Stats = {}



def to_Main_Menu(user_ID):
    """
    Вернуть пользователя в главное меню
    """
    logger.info(f"Sending Main Menu Keyboard For User {user_ID}")
    db_Manager.write_User_Position(user_ID, "main_Menu")
    user_Language = db_Manager.get_User_Language(user_ID)
    bot_Spotify_Sender.controls_Main_Menu(user_ID, language_Name=user_Language)



def in_Work(user_ID):
    """
    Поставить пользователю позицию in Work
    """
    logger.info(f"Sending In Work State For User {user_ID}")
    db_Manager.write_User_Position(user_ID, "work_In_Progress")
    user_Language = db_Manager.get_User_Language(user_ID)
    bot_Spotify_Sender.playlist_Preparing(user_ID, language_Name=user_Language)



def logout_Command(message):
    """
    Обработка команды выхода

    Удаление пользователя из всех таблиц в базе данных
    """
    user_ID = message.from_user.id
    if db_Manager.check_Bot_Reg(user_ID):
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)
        user_Language = db_Manager.get_User_Language(user_ID)
        logger.info(f"Preparing Logout For User {user_ID}")
        
        db_Manager.delete_User(user_Unique_ID, "bot_Users")
        db_Manager.delete_User(user_Unique_ID, "spotify_Users")
        db_Manager.delete_User(user_Unique_ID, "users_TopTracks")
        db_Manager.delete_User(user_Unique_ID, "users_TopArtists")

        logger.info(f"Logout Successful For User {user_ID}")
        bot_Spotify_Sender.user_Leaving(message.from_user.id, language_Name=user_Language)



def language_Command(message):
    """
    Обработка команды смены языка
    """
    user_ID = message.from_user.id
    if db_Manager.check_Spotify_Login(user_ID):
        user_ID = message.from_user.id
        logger.info(f"Sending Language Selector Keyboard For User {user_ID}")
        bot_Spotify_Sender.language_Selector(user_ID, db_Manager.get_User_Language(user_ID))
        db_Manager.write_User_Position(user_ID, "language_Select")



def menu_Command(message):
    """
    Обработка команды меню

    Если пользователь авторизован, вернуть его в главное меню
    """
    user_ID = message.from_user.id

    if db_Manager.check_Spotify_Login(user_ID):
        to_Main_Menu(user_ID)



def contacts_Command(message):
    """
    Обработка команды контактов

    Отправить пользователю контакты разработчика
    """
    user_ID = message.from_user.id

    logger.info(f"Sending Contacts For User {user_ID}")
    user_Language = db_Manager.get_User_Language(user_ID)
    bot_Spotify_Sender.send_Developer_Contacts(user_ID, language_Name=user_Language)






def create_Super_Shuffle(user_ID, language_Name, tracks_Count=None):
    """
    Создать супер-шаффл для пользователя

    user_ID - Telegram ID пользователя

    tracks_Count - Количество треков для супер-шафла (необязательный параметр, если параметра нет - выбираются все песни из Liked Songs)
    """
    try:
        in_Work(user_ID)
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)

        localization_Data = {
            "playlist_Name":language_Vocabluary[language_Name]["chat_Messages"]["superShuffle"]["your_SuperShuffle"],
            "playlist_Description":language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["playlist_Generated_ByJarvis"],
        }
    
        spotify_Service.check_User_Liked_Songs(user_Unique_ID, 200)
        playlist_ID = spotify_Service.super_Shuffle(user_Unique_ID, localization_Data=localization_Data, tracks_Count=tracks_Count)
        playlist_Data = spotify_Service.get_Playlist_Data(user_Unique_ID, playlist_ID)
        
        logger.info(f"Creating Super Shuffle For User {user_ID}")

    except spotify_Exceptions.no_Tracks:
        bot_Spotify_Sender.insufficient_Data_For_Shuffle(user_ID, language_Name=language_Name)

    except spotify_Exceptions.oauth_Http_Error:
        bot_Spotify_Sender.cannot_Authorize(user_ID, language_Name=language_Name)
        logger.error(f"HTTP ERROR OCCURED WHEN PREPARING SUPER SHUFFLE FOR USER {user_ID}")

    except spotify_Exceptions.oauth_Connection_Error:
        bot_Spotify_Sender.servers_Link_Error(user_ID, language_Name=language_Name)
        logger.error(f"CONNECTION ERROR OCCURED WHEN PREPARING SUPER SHUFFLE FOR USER {user_ID}")

    except:
        bot_Spotify_Sender.unknown_Error(user_ID, language_Name=language_Name)
        logger.error(f"UNKNOWN ERROR OCCURED WHEN PREPARING SUPER SHUFFLE FOR USER {user_ID}")

    else:
        playlist_Data["playlist_Cover"] = urllib.request.urlopen(playlist_Data["images"][1]["url"]).read() #Скачивание обложки

        bot_Spotify_Sender.playlist_Ready(user_ID, playlist_Data, language_Name=language_Name)
        logger.info(f"Super Shuffle Created Successfuly For User {user_ID}")

    finally:
        to_Main_Menu(user_ID)



def process_TopTracks_List(user_ID, time_Range, list_Page):
    """
    Подготовить данные для новой страницы Топ треков

    user_ID - Telegram ID пользователя

    list_Page - Страница списка данных
    """
    database_User_Tracks = db_Manager.search_In_Database(db_Manager.get_User_UniqueID(user_ID), "users_TopTracks", "user_Unique_ID")

    if database_User_Tracks: #Если у пользователя есть топ
        if time_Range == "short_term": #хахах, вот это костыли, вери найс гуд найс
            user_Tracks = database_User_Tracks[0][1]
        elif time_Range == "medium_term":
            user_Tracks = database_User_Tracks[0][2]
        elif time_Range == "long_term":
            user_Tracks = database_User_Tracks[0][3]

    top_Data = json.loads(user_Tracks) #Десериализуем строку в словарь
    max_Pages = math.ceil(len(top_Data["items"]) / 10) #Получаем кол-во страниц
    current_Page = {
        "current_Page":list_Page,
        "max_Pages":max_Pages,
        "time_Range":top_Data["top_Info"]["time_Range"],
        "last_Update":top_Data["top_Info"]["timestamp"],
        "items":{},
    }

    start_Index, stop_Index = ((10 * list_Page) - 10), (10 * list_Page) #ПОВЫШАЕМ ЧИТАЕМОСТЬ!
    for item in range(start_Index, stop_Index):
        if item < len(top_Data["items"]):
            current_Page["items"][item] = {
                "prefix":top_Data["items"][item]["prefix"],
                "artists":top_Data["items"][item]["artists"],
                "name":top_Data["items"][item]["name"]
            }

    return current_Page



def process_TopArtists_List(user_ID, time_Range, list_Page):
    """
    Подготовить данные для новой страницы Топ исполнителей

    user_ID - Telegram ID пользователя

    list_Page - Страница списка данных
    """
    database_User_Artists = db_Manager.search_In_Database(db_Manager.get_User_UniqueID(user_ID), "users_TopArtists", "user_Unique_ID")

    if database_User_Artists: #Если у пользователя есть топ
        if time_Range == "short_term": #хахах, вот это костыли, вери найс гуд найс
            user_Artists = database_User_Artists[0][1]
        elif time_Range == "medium_term":
            user_Artists = database_User_Artists[0][2]
        elif time_Range == "long_term":
            user_Artists = database_User_Artists[0][3]

    top_Data = json.loads(user_Artists) #Десериализуем строку в словарь
    max_Pages = math.ceil(len(top_Data["items"]) / 10) #Получаем кол-во страниц
    current_Page = {
        "current_Page":list_Page,
        "max_Pages":max_Pages,
        "time_Range":top_Data["top_Info"]["time_Range"],
        "last_Update":top_Data["top_Info"]["timestamp"],
        "items":{},
    }

    start_Index, stop_Index = ((10 * list_Page) - 10), (10 * list_Page) #ПОВЫШАЕМ ЧИТАЕМОСТЬ!
    for item in range(start_Index, stop_Index):
        if item < len(top_Data["items"]):
            current_Page["items"][item] = {
                "artist":top_Data["items"][item]["artist"],
                "followers":top_Data["items"][item]["followers"]
            }

    return current_Page



def user_Top_Tracks(user_ID, language_Name, time_Range):
    """
    Создать топ треков для пользователя

    user_ID - Telegram ID пользователя

    time_Range - Диапазон времени для выборки (short_term, medium_term, long_term)
    """
    try:
        top_Data = spotify_Service.get_User_Top_Tracks(db_Manager.get_User_UniqueID(user_ID), entities_Limit=50, time_Range=time_Range)
        logger.info(f"Get User Top Tracks For User {user_ID}")

    except spotify_Exceptions.no_Tops_Data:
        bot_Spotify_Sender.insufficient_Data_For_Top(user_ID, language_Name=language_Name)

    except spotify_Exceptions.oauth_Http_Error:
        bot_Spotify_Sender.cannot_Authorize(user_ID, language_Name=language_Name)
        logger.error(f"HTTP ERROR OCCURED WHEN PREPARING TOP TRACKS LIST FOR USER {user_ID}")

    except spotify_Exceptions.oauth_Connection_Error:
        bot_Spotify_Sender.servers_Link_Error(user_ID, language_Name=language_Name)
        logger.error(f"CONNECTION ERROR OCCURED WHEN PREPARING TOP TRACKS LIST FOR USER {user_ID}")

    except:
        bot_Spotify_Sender.unknown_Error(user_ID, language_Name=language_Name)
        logger.error(f"UNKNOWN ERROR OCCURED WHEN PREPARING TOP TRACKS LIST FOR USER {user_ID}")

    else:
        db_Manager.write_User_TopTracks(db_Manager.get_User_UniqueID(user_ID), data_Period=time_Range, top_Data=json.dumps(top_Data))

        try:
            bot_Spotify_Sender.tracks_Top(user_ID, process_TopTracks_List(user_ID, time_Range, 1), language_Name=language_Name)
        
        except:
            bot_Spotify_Sender.top_Database_Error(user_ID, language_Name=language_Name)
            logger.error(f"DATABASE ERROR OCCURED WHEN PREPARING TOP TRACKS LIST FOR USER {user_ID}")
        
        else:
            logger.info(f"Top Tracks Prepared Successfuly For User {user_ID}")

    finally:
        to_Main_Menu(user_ID)



def user_Top_Artists(user_ID, language_Name, time_Range):
    """
    Создать топ исполнителей для пользователя

    user_ID - Telegram ID пользователя

    time_Range - Диапазон времени для выборки (short_term, medium_term, long_term)
    """
    try:
        top_Data = spotify_Service.get_User_Top_Artists(db_Manager.get_User_UniqueID(user_ID), entities_Limit=50, time_Range=time_Range)
        logger.info(f"Get User Top Artists For User {user_ID}")

    except spotify_Exceptions.no_Tops_Data:
        bot_Spotify_Sender.insufficient_Data_For_Top(user_ID, language_Name=language_Name)

    except spotify_Exceptions.oauth_Http_Error:
        bot_Spotify_Sender.cannot_Authorize(user_ID, language_Name=language_Name)
        logger.error(f"HTTP ERROR OCCURED WHEN PREPARING TOP ARTISTS LIST FOR USER {user_ID}")

    except spotify_Exceptions.oauth_Connection_Error:
        bot_Spotify_Sender.servers_Link_Error(user_ID, language_Name=language_Name)
        logger.error(f"CONNECTION ERROR OCCURED WHEN PREPARING TOP ARTISTS LIST FOR USER {user_ID}")

    except:
        bot_Spotify_Sender.unknown_Error(user_ID, language_Name=language_Name)
        logger.error(f"UNKNOWN ERROR OCCURED WHEN PREPARING TOP ARTISTS LIST FOR USER {user_ID}")

    else:
        db_Manager.write_User_TopArtists(db_Manager.get_User_UniqueID(user_ID), data_Period=time_Range, top_Data=json.dumps(top_Data))

        try:
            bot_Spotify_Sender.artists_Top(user_ID, process_TopArtists_List(user_ID, time_Range, 1), language_Name=language_Name)
        
        except:
            bot_Spotify_Sender.top_Database_Error(user_ID, language_Name=language_Name)
            logger.error(f"DATABASE ERROR OCCURED WHEN PREPARING TOP ARTISTS LIST FOR USER {user_ID}")
        
        else:
            logger.info(f"Top Artists Prepared Successfuly For User {user_ID}")

    finally:
        to_Main_Menu(user_ID)



def create_Top_Playlist(user_ID, time_Range, language_Name):
    """
    Создать плейлист из топ треков для пользователя

    user_ID - Telegram ID пользователя

    time_Range - Диапазон времени для выборки (short_term, medium_term, long_term)
    """
    try:
        in_Work(user_ID)
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)

        localization_Data = {
            "playlist_Name":language_Vocabluary[language_Name]["chat_Messages"]["yourTops"]["your_TopSongs"],
            "playlist_TimeRange":language_Vocabluary[language_Name]["chat_Messages"]["yourTops"][time_Range],
            "playlist_Description":language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["playlist_Generated_ByJarvis"],
        }

        playlist_ID = spotify_Service.create_Top_Tracks_Playlist(user_Unique_ID, localization_Data=localization_Data, time_Range=time_Range)
        playlist_Data = spotify_Service.get_Playlist_Data(user_Unique_ID, playlist_ID)
        logger.info(f"Creating Top Tracks Playlist For User {user_ID}")

    except spotify_Exceptions.oauth_Http_Error:
        bot_Spotify_Sender.cannot_Authorize(user_ID, language_Name=language_Name)
        logger.error(f"HTTP ERROR OCCURED WHEN PREPARING TOP TRACKS PLAYLIST FOR USER {user_ID}")

    except spotify_Exceptions.oauth_Connection_Error:
        bot_Spotify_Sender.servers_Link_Error(user_ID, language_Name=language_Name)
        logger.error(f"CONNECTION ERROR OCCURED WHEN PREPARING TOP TRACKS PLAYLIST FOR USER {user_ID}")

    except:
        bot_Spotify_Sender.unknown_Error(user_ID, language_Name=language_Name)
        logger.error(f"UNKNOWN ERROR OCCURED WHEN PREPARING TOP TRACKS PLAYLIST FOR USER {user_ID}")

    else:
        playlist_Data["playlist_Cover"] = urllib.request.urlopen(playlist_Data["images"][1]["url"]).read() #Скачивание обложки

        bot_Spotify_Sender.playlist_Ready(user_ID, playlist_Data, language_Name=language_Name)
        logger.info(f"Top Tracks Playlist Created Successfuly For User {user_ID}")
    
    finally:
        to_Main_Menu(user_ID)



def process_MusicQuiz_Round(user_ID, language_Name, game_Round):
    """
    Подготовить массив данных для раунда музыкальной викторины

    user_ID - Telegram ID пользователя

    game_Round - Номер раунда музыкальной викторины
    """
    try:
        musicQuiz_Keyboard_Items = []
        musicQuiz_Keyboard_Items.append(musicQuiz_User_Songs[user_ID]["right_Answers"][game_Round])

        list_Size = len(musicQuiz_User_Songs[user_ID]["other_Answers"]) - 1

        key_Indexes = [] #Генерация массива из 3 цифр для поиска 3 случайных ключей в клавиатуру
        while len(key_Indexes) < 3:
            index = random.randint(10, list_Size)
            if index not in key_Indexes:
                key_Indexes.append(index)

        for index in range(3): #Добавление 3 случайных вариантов ответа в клавиатуру
            answer_Item = key_Indexes[index]
            musicQuiz_Keyboard_Items.append(musicQuiz_User_Songs[user_ID]["other_Answers"][answer_Item])

        random.shuffle(musicQuiz_Keyboard_Items) #Перемешивание клавиатуры

        audio_File = urllib.request.urlopen(musicQuiz_User_Songs[user_ID]["right_Answers"][game_Round]["audio_URL"]).read()

        musicQuiz_Round_Data = {
            "current_Round":game_Round,
            "audio_File":audio_File,
        }

        keyboard_Keys = []
        for key in range(4): #Перевод данных клавиатуры в человеческий вид
            keyboard_Keys.append(musicQuiz_Keyboard_Items[key]["artists"] + " - " + musicQuiz_Keyboard_Items[key]["name"])

        musicQuiz_Round_Data["keyboard"] = keyboard_Keys
        musicQuiz_User_Stats[user_ID].update({
            "game_Round":game_Round,
            "round_Prepared_Timestamp":int(time.time()),
            "round_Answer":musicQuiz_User_Songs[user_ID]["right_Answers"][game_Round]["artists"] + " - " + musicQuiz_User_Songs[user_ID]["right_Answers"][game_Round]["name"],
        })
        
    except:
        logger.error(f"ERROR OCCURED WHEN PROCESSING MUSIC QUIZ FOR USER {user_ID}")
        bot_Spotify_Sender.musicQuiz_Error_RoundProcess(user_ID, language_Name=language_Name)
        to_Main_Menu(user_ID)

    else:
        bot_Spotify_Sender.send_MusicQuiz_Round(user_ID, musicQuiz_Round_Data, language_Name=language_Name)



def create_MusicQuiz_Top_Tracks(user_ID, language_Name, time_Range):
    """
    Подготовить выборку из топ треков для музыкальной викторины

    user_ID - Telegram ID пользователя

    time_Range - Диапазон времени для выборки (short_term, medium_term, long_term)
    """
    try:
        db_Manager.write_User_Position(user_ID, "work_In_Progress")
        musicQuiz_Data = spotify_Service.create_MusicQuiz_Top_Tracks(db_Manager.get_User_UniqueID(user_ID), time_Range)
        logger.info(f"Creating Top Tracks Music Quiz For User {user_ID}")

    except spotify_Exceptions.no_Tops_Data:
        bot_Spotify_Sender.insufficient_Data_For_MusicQuiz(user_ID, language_Name=language_Name)
        to_Main_Menu(user_ID)

    except spotify_Exceptions.oauth_Http_Error:
        bot_Spotify_Sender.cannot_Authorize(user_ID, language_Name=language_Name)
        logger.error(f"HTTP ERROR OCCURED WHEN PREPARING TOP TRACKS MUSIC QUIZ FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    except spotify_Exceptions.oauth_Connection_Error:
        bot_Spotify_Sender.servers_Link_Error(user_ID, language_Name=language_Name)
        logger.error(f"CONNECTION ERROR OCCURED WHEN PREPARING TOP TRACKS MUSIC QUIZ FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    except spotify_Exceptions.musicQuiz_Error_NoTracks:
        bot_Spotify_Sender.musicQuiz_Error_NoTracks(user_ID, language_Name=language_Name)
        logger.error(f"MUSIC QUIZ ERROR WHEN PREPARING GAME FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    except:
        bot_Spotify_Sender.unknown_Error(user_ID, language_Name=language_Name)
        logger.error(f"UNKNOWN ERROR OCCURED WHEN PREPARING TOP TRACKS MUSIC QUIZ FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    else:
        musicQuiz_User_Songs[user_ID] = musicQuiz_Data
        musicQuiz_User_Stats[user_ID] = {
            "game_Round":0,
            "round_Prepared_Timestamp":0,
            "round_Answer":"",
            "correct_Answers":0,
            "total_Rounds":10,
        }
        db_Manager.write_User_Position(user_ID, "user_MusicQuiz_inGame")
        process_MusicQuiz_Round(user_ID, language_Name=language_Name, game_Round=0)



def create_MusicQuiz_Liked_Songs(user_ID, language_Name):
    """
    Подготовить выборку из Liked Songs для музыкальной викторины

    user_ID - Telegram ID пользователя
    """
    try:
        db_Manager.write_User_Position(user_ID, "work_In_Progress")
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)
        spotify_Service.check_User_Liked_Songs(user_Unique_ID, 50)
        musicQuiz_Data = spotify_Service.create_MusicQuiz_Liked_Songs(user_Unique_ID)
        logger.info(f"Creating Liked Songs Music Quiz For User {user_ID}")

    except spotify_Exceptions.no_Tracks:
        bot_Spotify_Sender.insufficient_Data_For_MusicQuiz(user_ID, language_Name=language_Name)
        to_Main_Menu(user_ID)

    except spotify_Exceptions.oauth_Http_Error:
        bot_Spotify_Sender.cannot_Authorize(user_ID, language_Name=language_Name)
        logger.error(f"HTTP ERROR OCCURED WHEN PREPARING LIKED SONGS MUSIC QUIZ FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    except spotify_Exceptions.oauth_Connection_Error:
        bot_Spotify_Sender.servers_Link_Error(user_ID, language_Name=language_Name)
        logger.error(f"CONNECTION ERROR OCCURED WHEN PREPARING LIKED SONGS MUSIC QUIZ FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    except spotify_Exceptions.musicQuiz_Error_NoTracks:
        bot_Spotify_Sender.musicQuiz_Error_NoTracks(user_ID, language_Name=language_Name)
        logger.error(f"MUSIC QUIZ ERROR WHEN PREPARING GAME FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    except:
        bot_Spotify_Sender.unknown_Error(user_ID, language_Name=language_Name)
        logger.error(f"UNKNOWN ERROR OCCURED WHEN PREPARING LIKED SONGS MUSIC QUIZ FOR USER {user_ID}")
        to_Main_Menu(user_ID)

    else:
        musicQuiz_User_Songs[user_ID] = musicQuiz_Data
        musicQuiz_User_Stats[user_ID] = {
            "game_Round":0,
            "round_Prepared_Timestamp":0,
            "round_Answer":"",
            "correct_Answers":0,
            "total_Rounds":10,
        }
        db_Manager.write_User_Position(user_ID, "user_MusicQuiz_inGame")
        process_MusicQuiz_Round(user_ID, language_Name=language_Name, game_Round=0)



logger.info("Spotify Module Ready")



def callback_Handler(callback_Data):
    user_ID = callback_Data.from_user.id
    logger.info(f"New Callback Data: {callback_Data.data} From: {user_ID}")

    if db_Manager.check_Spotify_Login(user_ID):
        user_Language = db_Manager.get_User_Language(user_ID) #Записать в переменную язык пользователя
        callback_Request = callback_Data.data.split("#") #Парсим строку

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
                
                except spotify_Exceptions.oauth_Http_Error:
                    bot_Spotify_Sender.cannot_Authorize(user_ID, language_Name=user_Language)

                except:
                    bot_Spotify_Sender.unknown_Error(user_ID, language_Name=user_Language)
                
                else:
                    if callback_Request[2] == "album" or callback_Request[2] == "artist" or callback_Request[2] == "playlist":
                        bot_Spotify_Sender.playback_Started(user_ID, language_Name=user_Language)
                    
                    elif callback_Request[2] == "track":
                        bot_Spotify_Sender.song_Added_To_Queue(user_ID, language_Name=user_Language)
        
        if callback_Data.message: #По каким-то причинам у сообщений отправленных из Inline нету тела сообщения
            message_ID = callback_Data.message.message_id

            if callback_Request[0] == "interface": #Если сообщение из раздела интерфейса
                if callback_Request[1] == "topTracks":
                    if callback_Request[2] == "createPlaylist":
                            create_Top_Playlist(user_ID, time_Range=callback_Request[3], language_Name=user_Language)
                    
                    elif callback_Request[2] == "page":
                        page_Number = int(callback_Request[4])
                        top_Data = process_TopTracks_List(user_ID, time_Range=callback_Request[3], list_Page=page_Number)
                        bot_Spotify_Sender.tracks_Top(user_ID, top_Data, language_Name=user_Language, message_ID=message_ID)
                
                elif callback_Request[1] == "topArtists":
                    if callback_Request[2] == "page":
                        page_Number = int(callback_Request[4])
                        top_Data = process_TopArtists_List(user_ID, time_Range=callback_Request[3], list_Page=page_Number)
                        bot_Spotify_Sender.artists_Top(user_ID, top_Data, language_Name=user_Language, message_ID=message_ID)



def inline_Handler(data):
    user_ID = data.from_user.id
    inline_ID = data.id
    inline_Request = data.query.lower()

    if db_Manager.check_Spotify_Login(user_ID):
        user_Language = db_Manager.get_User_Language(user_ID)
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)

        if inline_Request == "share song":
            try:
                user_Data = spotify_Service.get_Current_Playing(user_Unique_ID)

            except spotify_Exceptions.no_Data:
                bot_Spotify_Sender.inline_NowPlaying_Error(inline_ID, language_Name=user_Language)

            except spotify_Exceptions.no_Playback:
                bot_Spotify_Sender.inline_NowPlaying_Nothing(inline_ID, language_Name=user_Language)

            except spotify_Exceptions.private_Session_Enabled:
                bot_Spotify_Sender.inline_Private_Session(inline_ID, language_Name=user_Language)

            except spotify_Exceptions.oauth_Http_Error:
                bot_Spotify_Sender.inline_Auth_Error(inline_ID, language_Name=user_Language)
                logger.error(f"INLINE MODE ERROR. OAUTH ERROR WHEN SENDING NOW PLAYING FOR USER {user_ID}")

            except:
                bot_Spotify_Sender.inline_Unknown_Error(inline_ID, language_Name=user_Language)
                logger.error(f"INLINE MODE ERROR. UNKNOWN ERROR WHEN SENDING NOW PLAYING FOR USER {user_ID}")
            
            else:
                bot_Spotify_Sender.share_Inline_NowPlaying(inline_ID, user_Data, language_Name=user_Language)
        
        if inline_Request == "share context":
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

            except spotify_Exceptions.oauth_Http_Error:
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

    
    else:
        bot_Spotify_Sender.inline_Spotify_Not_Authorized(inline_ID, language_Name=user_Language)



def chat_Messages_Handler(message):
    user_ID = message.from_user.id
    logger.info(f"New Message: {message.text} From: {message.from_user.id}")

    if not db_Manager.check_Bot_Reg(user_ID): #Если в базе данных его нет, регистрируем
        logger.info(f"User {user_ID} Not In Reg Table. Registration...")
        reg_Timestamp = int(time.time())

        language_Code = message.from_user.language_code

        if language_Code == "ru" or language_Code == "uk" or language_Code == "be": #Русский, украинский, беларусский
            user_Language = "RUS"
        else:
            user_Language = "ENG"

        generated_Unique_ID = db_Manager.generate_Unique_ID()
        db_Manager.register_User(user_ID, generated_Unique_ID, user_Language, bot_Version, reg_Timestamp)



    #Оптимизация для БД
    user_Position_Cache = db_Manager.get_User_Position(user_ID) #Записать в переменную позицию пользователя
    user_Language = db_Manager.get_User_Language(user_ID) #Записать в переменную язык пользователя



    if not db_Manager.check_Spotify_Login(user_ID): #Если пользователь еще не вошел в Spotify, предлагаем войти
        logger.info(f"User {user_ID} Not In Spotify Table. Sending Offer For Login")
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)
        spotify_Auth_Link = spotify_Oauth.generate_Auth_Link(user_Unique_ID)
        bot_Spotify_Sender.spotify_Login_Offer(user_ID, spotify_Auth_Link, language_Name=user_Language)



    if db_Manager.check_Spotify_Login(user_ID):
        logger.info(f"User {user_ID} Have Spotify Login")


        #Заглушка если in Work позиция
        if user_Position_Cache == "work_In_Progress":
            bot_Spotify_Sender.denied_Work_Reason(user_ID, language_Name=user_Language)


        #Меню смены языка
        if user_Position_Cache == "language_Select":
            if message.text == "English":
                db_Manager.write_User_Language(user_ID, "ENG")
                bot_Spotify_Sender.language_Changed(user_ID, "ENG")
                to_Main_Menu(user_ID)

            elif message.text == "Russian":
                db_Manager.write_User_Language(user_ID, "RUS")
                bot_Spotify_Sender.language_Changed(user_ID, "RUS")
                to_Main_Menu(user_ID)
            
            else:
                bot_Spotify_Sender.astray_Notification(user_ID, db_Manager.get_User_Language(user_ID))


        if db_Manager.get_User_BotVersion(user_ID) < bot_Version: #Если версия клавиатуры пользователя старая, то перемещаем в главное меню
            to_Main_Menu(user_ID)
            bot_Spotify_Sender.jarvis_Updated(user_ID, language_Name=user_Language, jarvis_Version=bot_Version)
            db_Manager.write_User_BotVersion(user_ID, bot_Version)


        #ГЛАВНОЕ МЕНЮ


        if user_Position_Cache == "main_Menu":
            if message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["now_Playing"]: #Пункт Now Playing
                logger.info(f"User {user_ID} Entered To Now Playing")
                try:
                    user_Data = spotify_Service.get_Current_Playing(db_Manager.get_User_UniqueID(user_ID))

                except spotify_Exceptions.no_Playback:
                    bot_Spotify_Sender.nowplaying_Nothing(user_ID, language_Name=user_Language)

                except spotify_Exceptions.no_Data:
                    bot_Spotify_Sender.now_Playing_Error(user_ID, language_Name=user_Language)
                
                except spotify_Exceptions.private_Session_Enabled:
                    bot_Spotify_Sender.private_Session_Enabled(user_ID, language_Name=user_Language)

                except spotify_Exceptions.oauth_Http_Error:
                    bot_Spotify_Sender.cannot_Authorize(user_ID, language_Name=user_Language)
                    logger.error(f"HTTP ERROR OCCURED WHEN SENDING NOW PLAYING FOR USER {user_ID}")

                except spotify_Exceptions.oauth_Connection_Error:
                    bot_Spotify_Sender.servers_Link_Error(user_ID, language_Name=user_Language)
                    logger.error(f"CONNECTION ERROR OCCURED WHEN SENDING NOW PLAYING FOR USER {user_ID}")

                else:
                    user_Data["song_Cover"] = urllib.request.urlopen(user_Data["images"][1]["url"]).read() #Скачивание обложки

                    if user_Data["preview_URL"]:
                        user_Data["preview_File"] = urllib.request.urlopen(user_Data["preview_URL"]).read() #Скачивание превью

                    bot_Spotify_Sender.now_Playing(user_ID, user_Data, language_Name=user_Language)
                    logger.info(f"Sending Now Playing For User {user_ID}")

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["super_Shuffle"]: #Пункт Супер-шаффла
                logger.info(f"User {user_ID} Entered To Super Shuffle")
                db_Manager.write_User_Position(user_ID, "user_Super_Shuffle")
                bot_Spotify_Sender.superShuffle_Description(user_ID, language_Name=user_Language)
                bot_Spotify_Sender.shuffle_Tracks_Count(user_ID, language_Name=user_Language)
                logger.info(f"Sending Super Shuffle Selector For User {user_ID}")

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["your_Tops"]: #Пункт топов
                logger.info(f"User {user_ID} Entered To Your Tops")
                db_Manager.write_User_Position(user_ID, "user_Your_Tops")
                bot_Spotify_Sender.yourTops_Description(user_ID, language_Name=user_Language)
                bot_Spotify_Sender.tops_Type_Select(user_ID, language_Name=user_Language)
                logger.info(f"Sending Your Tops Selector For User {user_ID}")
            
            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["musicQuiz"]: #Пункт музыкальной викторины
                logger.info(f"User {user_ID} Entered To Music Quiz")
                db_Manager.write_User_Position(user_ID, "user_MusicQuiz_Type")
                bot_Spotify_Sender.musicQuiz_Rules(user_ID, language_Name=user_Language)
                bot_Spotify_Sender.musicQuiz_Type_Select(user_ID, language_Name=user_Language)
                logger.info(f"Sending Music Quiz Type Selector For User {user_ID}")

            else:
                bot_Spotify_Sender.astray_Notification(user_ID, language_Name=user_Language)


        #ПУНКТ СУПЕР-ШАФФЛА


        if user_Position_Cache == "user_Super_Shuffle":
            if message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["offset_Size"]["100_Songs"]:
                create_Super_Shuffle(user_ID, language_Name=user_Language, tracks_Count=100)

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["offset_Size"]["200_Songs"]:
                create_Super_Shuffle(user_ID, language_Name=user_Language, tracks_Count=200)

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["offset_Size"]["all_Offset"]:
                create_Super_Shuffle(user_ID, language_Name=user_Language)

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"]:
                to_Main_Menu(user_ID)
            
            else:
                bot_Spotify_Sender.astray_Notification(user_ID, language_Name=user_Language)


        #ПУНКТ ТОПОВ


        if user_Position_Cache == "user_Your_Tops":
            if message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["songs"]:
                bot_Spotify_Sender.tops_Time_Period(user_ID, language_Name=user_Language)
                db_Manager.write_User_Position(user_ID, "user_Top_Tracks_Time")

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["artists"]:
                bot_Spotify_Sender.tops_Time_Period(user_ID, language_Name=user_Language)
                db_Manager.write_User_Position(user_ID, "user_Top_Artists_Time")

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"]:
                to_Main_Menu(user_ID)

            else:
                bot_Spotify_Sender.astray_Notification(user_ID, language_Name=user_Language)



        if user_Position_Cache == "user_Top_Tracks_Time":
            if message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["time_Buttons"]["4_Weeks"]:
                user_Top_Tracks(user_ID, language_Name=user_Language, time_Range="short_term")

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["time_Buttons"]["6_Months"]:
                user_Top_Tracks(user_ID, language_Name=user_Language, time_Range="medium_term")

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["time_Buttons"]["all_Time"]:
                user_Top_Tracks(user_ID, language_Name=user_Language, time_Range="long_term")

            else:
                bot_Spotify_Sender.astray_Notification(user_ID, language_Name=user_Language)



        if user_Position_Cache == "user_Top_Artists_Time":
            if message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["time_Buttons"]["4_Weeks"]:
                user_Top_Artists(user_ID, language_Name=user_Language, time_Range="short_term")

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["time_Buttons"]["6_Months"]:
                user_Top_Artists(user_ID, language_Name=user_Language, time_Range="medium_term")

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["time_Buttons"]["all_Time"]:
                user_Top_Artists(user_ID, language_Name=user_Language, time_Range="long_term")

            else:
                bot_Spotify_Sender.astray_Notification(user_ID, language_Name=user_Language)



        #ПУНКТ МУЗЫКАЛЬНОЙ ВИКТОРИНЫ



        if user_Position_Cache == "user_MusicQuiz_Type":
            if message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["liked_Songs"]:
                bot_Spotify_Sender.musicQuiz_Preparing(user_ID, language_Name=user_Language)
                create_MusicQuiz_Liked_Songs(user_ID, language_Name=user_Language)

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["top_Songs"]:
                db_Manager.write_User_Position(user_ID, "user_MusicQuiz_Time")
                bot_Spotify_Sender.tops_Time_Period(user_ID, language_Name=user_Language)

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"]:
                to_Main_Menu(user_ID)

            else:
                bot_Spotify_Sender.astray_Notification(user_ID, language_Name=user_Language)

        if user_Position_Cache == "user_MusicQuiz_Time":
            if message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["time_Buttons"]["4_Weeks"]:
                bot_Spotify_Sender.musicQuiz_Preparing(user_ID, language_Name=user_Language)
                create_MusicQuiz_Top_Tracks(user_ID, language_Name=user_Language, time_Range="short_term")

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["time_Buttons"]["6_Months"]:
                bot_Spotify_Sender.musicQuiz_Preparing(user_ID, language_Name=user_Language)
                create_MusicQuiz_Top_Tracks(user_ID, language_Name=user_Language, time_Range="medium_term")

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["time_Buttons"]["all_Time"]:
                bot_Spotify_Sender.musicQuiz_Preparing(user_ID, language_Name=user_Language)
                create_MusicQuiz_Top_Tracks(user_ID, language_Name=user_Language, time_Range="long_term")

            else:
                bot_Spotify_Sender.astray_Notification(user_ID, language_Name=user_Language)
        
        if user_Position_Cache == "user_MusicQuiz_inGame":
            if message.text == musicQuiz_User_Stats[user_ID]["round_Answer"]: #Если сообщение пользователя = правильный ответ
                if (int(time.time()) - musicQuiz_User_Stats[user_ID]["round_Prepared_Timestamp"]) <= 10: #Если с момента создания раунда прошло не более 10 секунд включительно
                    bot_Spotify_Sender.musicQuiz_Correct_Answer(user_ID, musicQuiz_User_Stats[user_ID], language_Name=user_Language) #Засчитать ответ
                    musicQuiz_User_Stats[user_ID]["correct_Answers"] += 1
                else:
                    bot_Spotify_Sender.musicQuiz_Answer_Timeout(user_ID, musicQuiz_User_Stats[user_ID], language_Name=user_Language) #Иначе поражение

            else:
                bot_Spotify_Sender.musicQuiz_Incorrect_Answer(user_ID, musicQuiz_User_Stats[user_ID], language_Name=user_Language) #Поражение если ответ неправильный



            musicQuiz_User_Stats[user_ID]["game_Round"] += 1



            if musicQuiz_User_Stats[user_ID]["game_Round"] < musicQuiz_User_Stats[user_ID]["total_Rounds"]: #Пока раунд < кол-во раундов, отправлять раунды, иначе отправить конец викторины и вернуть в главное меню
                process_MusicQuiz_Round(user_ID, language_Name=user_Language, game_Round=musicQuiz_User_Stats[user_ID]["game_Round"])
            else:
                bot_Spotify_Sender.musicQuiz_End(user_ID, musicQuiz_User_Stats[user_ID], language_Name=user_Language)
                to_Main_Menu(user_ID)