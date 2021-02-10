import math
import time
import json
import random
from libraries import database_Manager
from libraries import spotify_Api
from libraries import spotify_Oauth
from libraries import youtube_Lib
from spotify_Module import spotify_Exceptions



def check_Token_Lifetime(user_Unique_ID):
    """
    Проверить жив ли еще токен, если токен мертв, обновить его

    user_Unique_ID - Внутренний уникальный ID пользователя
    """
    current_Timestamp = int(time.time())
    last_Refresh_Timestamp = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][7]

    if (current_Timestamp - (last_Refresh_Timestamp - 60)) > 3600:
        spotify_Oauth.refresh_Access_Token(user_Unique_ID)



def get_Current_Playing(user_Unique_ID):
    """
    Получить текущее проигрывание пользователя, в случае успеха возвращает словарь

    В случае ошибки возвращает исключения:
    no_Playback - ничего не играет
    no_Data - не хватает мета-данных
    private_Session_Enabled - активирована приватная сессия

    user_Unique_ID - Внутренний уникальный ID пользователя
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    user_Playback = spotify_Api.get_Current_Playback(user_Auth_Token)

    if user_Playback["device"]["is_private_session"]:
        raise spotify_Exceptions.private_Session_Enabled

    try:
        playback_Data = {"artists":[]}

        for artist in range(len(user_Playback["item"]["artists"])):
            playback_Data["artists"] += [user_Playback["item"]["artists"][artist]["name"]]

        playback_Data["album_Name"] = user_Playback["item"]["album"]["name"]
        playback_Data["song_Name"] = user_Playback["item"]["name"]
        playback_Data["song_Duration"] = user_Playback["item"]["duration_ms"]
        playback_Data["release_Date"] = user_Playback["item"]["album"]["release_date"]
        playback_Data["song_ID"] = user_Playback["item"]["id"]
        playback_Data["external_URL"] = user_Playback["item"]["external_urls"]["spotify"]
        playback_Data["preview_URL"] = user_Playback["item"]["preview_url"]
        playback_Data["images"] = user_Playback["item"]["album"]["images"]

        search_Keywords = ", ".join(playback_Data["artists"]) + " " + playback_Data["song_Name"]
        try: #Костыль для обхода привышения квоты на поиск. КОГДА НИБУДЬ сделаю авторизацию через Гугл аккаунт... КОГДА НИБУДЬ))
            search_Result = youtube_Lib.search_Youtube(search_Keywords) #Поиск Ютуб клипа для песни
        
        except:
            playback_Data["youtube_URL"] = ""
        
        else:
            if search_Result["items"]: #Если песня найдена
                first_Result_ID = search_Result["items"][0]["id"]["videoId"]
                playback_Data["youtube_URL"] = "https://youtu.be/" + first_Result_ID
            else:
                playback_Data["youtube_URL"] = ""

    except:
        raise spotify_Exceptions.no_Data
    
    else:
        return playback_Data



def get_Current_Context(user_Unique_ID):
    """
    Получить текущий контекст пользователя

    В случае ошибки возвращает исключения:
    no_Playback - ничего не играет
    no_Playing_Context - нет активного контекста
    private_Session_Enabled - активирована приватная сессия

    user_Unique_ID - Внутренний уникальный ID пользователя
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    user_Playback = spotify_Api.get_Current_Playback(user_Auth_Token)

    if user_Playback["device"]["is_private_session"]:
        raise spotify_Exceptions.private_Session_Enabled

    playback_Data = {}

    if user_Playback["context"]:
        playback_Data["context_URI"] = user_Playback["context"]["uri"]
        playback_Data["context_Type"] = user_Playback["context"]["type"] #Context type может быть исполнитель, альбом, или плейлист

        return playback_Data
    else:
        raise spotify_Exceptions.no_Playing_Context




def start_Playback(user_Unique_ID, playback_Context=None, playback_Uris=None):
    """
    Начинает воспроизведение контента, в случае успеха возвращает True

    В случае ошибки возвращает исключения:
    no_ActiveDevices - Нет активных устройств
    premium_Required - Требуется премиум-подписка

    user_Unique_ID - Внутренний уникальный ID пользователя

    playback_Context - Контекст для проигрывания (плейлист, исполнитель)
    
    ИЛИ

    playback_Uris - Список из URI треков Спотифай
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    user_Devices = spotify_Api.get_User_Devices(user_Auth_Token)

    if not user_Devices["devices"]: #Проверка наличия активного устройства
        raise spotify_Exceptions.no_ActiveDevices

    try:
        if playback_Context:
            spotify_Api.start_Playback(user_Auth_Token, playback_Context=playback_Context)
        elif playback_Uris:
            spotify_Api.start_Playback(user_Auth_Token, playback_Uris=playback_Uris)

    except spotify_Exceptions.http_Error as error:
        if error.http_Code == 404:
            raise spotify_Exceptions.no_ActiveDevices
        
        elif error.http_Code == 403:
            raise spotify_Exceptions.premium_Required

    else:
        return True



def add_Track_To_Queue(user_Unique_ID, track_Uri):
    """
    Добавить трек в очередь проигрывания пользователя

    В случае ошибки возвращает исключения:
    no_ActiveDevices - Нет активных устройств
    premium_Required - Требуется премиум-подписка

    user_Unique_ID - Внутренний уникальный ID пользователя

    track_Uri - URI песни
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    user_Devices = spotify_Api.get_User_Devices(user_Auth_Token)

    if not user_Devices["devices"]: #Проверка наличия активного устройства
        raise spotify_Exceptions.no_ActiveDevices
    
    try:
        spotify_Api.add_Track_To_Queue(user_Auth_Token, track_Uri=track_Uri)

    except spotify_Exceptions.http_Error as error:
        if error.http_Code == 404:
            raise spotify_Exceptions.no_ActiveDevices
        
        elif error.http_Code == 403:
            raise spotify_Exceptions.premium_Required

    else:
        return True



def get_Playlist_Data(user_Unique_ID, playlist_ID):
    """
    Возвращает информацию о плейлисте по ID

    user_Unique_ID - Внутренний уникальный ID пользователя

    playlist_ID - Уникальный ID плейлиста в Spotify
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    playlist_Info = spotify_Api.get_Playlist_Info(user_Auth_Token, playlist_ID)

    playlist_Data = {}
    playlist_Data["name"] = playlist_Info["name"]
    playlist_Data["description"] = playlist_Info["description"]
    playlist_Data["external_URL"] = playlist_Info["external_urls"]["spotify"]
    playlist_Data["playlist_ID"] = playlist_Info["id"]
    playlist_Data["total_Tracks"] = playlist_Info["tracks"]["total"]
    playlist_Data["images"] = playlist_Info["images"]

    return playlist_Data



def get_Album_Data(user_Unique_ID, album_ID):
    """
    Возвращает информацию о альбоме по ID

    user_Unique_ID - Внутренний уникальный ID пользователя

    album_ID - Уникальный ID плейлиста в Spotify
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    album_Info = spotify_Api.get_Album_Info(user_Auth_Token, album_ID)

    album_Data = {"artists":[]}

    for artist in range(len(album_Info["artists"])):
        album_Data["artists"] += [album_Info["artists"][artist]["name"]]

    album_Data["external_URL"] = album_Info["external_urls"]["spotify"]
    album_Data["id"] = album_Info["id"]
    album_Data["images"] = album_Info["images"]
    album_Data["label"] = album_Info["label"]
    album_Data["name"] = album_Info["name"]
    album_Data["release_Date"] = album_Info["release_date"]
    album_Data["total_Tracks"] = album_Info["total_tracks"]

    return album_Data



def get_Artist_Data(user_Unique_ID, artist_ID):
    """
    Возвращает информацию о исполнителе по ID

    user_Unique_ID - Внутренний уникальный ID пользователя

    artist_ID - Уникальный ID исполнителя в Spotify
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    artist_Info = spotify_Api.get_Artist_Info(user_Auth_Token, artist_ID)

    artist_Data = {"genres":[]}

    for genre in range(len(artist_Info["genres"])):
        artist_Data["genres"] += [artist_Info["genres"][genre]]

    artist_Data["external_URL"] = artist_Info["external_urls"]["spotify"]
    artist_Data["followers"] = artist_Info["followers"]["total"]
    artist_Data["id"] = artist_Info["id"]
    artist_Data["images"] = artist_Info["images"]
    artist_Data["name"] = artist_Info["name"]

    return artist_Data



def check_User_Liked_Songs(user_Unique_ID, minimum_Count):
    """
    Проверяет есть ли у пользователя минимальное кол-во Liked Songs, в случае успеха возвращает True

    В случае ошибки возвращает исключение no_Tracks (треков не хватает)

    user_Unique_ID - Внутренний уникальный ID пользователя

    minimum_Count - Кол-во треков
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    user_Data = spotify_Api.get_Saved_Tracks(user_Auth_Token)

    if user_Data["total"] >= minimum_Count:
        return True
    else:
        raise spotify_Exceptions.no_Tracks



def search_Item(user_Unique_ID, search_Query, search_Types="track", limit=5, offset=0):
    """
    Поиск в Spotify

    В случае ошибки возвращает исключения oauth_Connection_Error, oauth_Http_Error, oauth_Unknown_Error

    user_Unique_ID - Внутренний уникальный ID пользователя

    search_Query - Поисковой запрос

    search_Types - Типы для поиска, исполнитель, альбом, трек

    limit - Лимит элементов поиска

    offset - Смещение элементов поиска
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    search_Data = spotify_Api.search_Item(user_Auth_Token, search_Query, search_Types, limit, offset)

    total_Results = 0
    for search_Type in search_Data:
        total_Results += search_Data[search_Type]["total"]
        
        if not total_Results:
            raise spotify_Exceptions.search_No_Results
    
    search_Results = {
        "albums":[],
        "artists":[],
        "tracks":[],
        "playlists":[],
    }
    for search_Type, _ in search_Data.items():
        if search_Type == "albums":
            for album in range(len(search_Data[search_Type]["items"])):
                album_Item = search_Data[search_Type]["items"][album]

                album_Data = {"artists":[]}

                for artist in range(len(album_Item["artists"])):
                    album_Data["artists"] += [album_Item["artists"][artist]["name"]]

                album_Data["external_URL"] = album_Item["external_urls"]["spotify"]
                album_Data["id"] = album_Item["id"]
                album_Data["images"] = album_Item["images"]
                album_Data["name"] = album_Item["name"]
                album_Data["release_Date"] = album_Item["release_date"]
                album_Data["total_Tracks"] = album_Item["total_tracks"]

                search_Results["albums"].append(album_Data)

        elif search_Type == "artists":
            for artist in range(len(search_Data[search_Type]["items"])):
                artist_Item = search_Data[search_Type]["items"][artist]

                artist_Data = {"genres":[]}

                for genre in range(len(artist_Item["genres"])):
                    artist_Data["genres"] += [artist_Item["genres"][genre]]

                artist_Data["external_URL"] = artist_Item["external_urls"]["spotify"]
                artist_Data["followers"] = artist_Item["followers"]["total"]
                artist_Data["id"] = artist_Item["id"]
                artist_Data["images"] = artist_Item["images"]
                artist_Data["name"] = artist_Item["name"]

                search_Results["artists"].append(artist_Data)

        elif search_Type == "tracks":
            for track in range(len(search_Data[search_Type]["items"])):
                track_Item = search_Data[search_Type]["items"][track]

                track_Data = {"artists":[]}
                for artist in range(len(track_Item["artists"])):
                    track_Data["artists"] += [track_Item["artists"][artist]["name"]]

                track_Data["album_Name"] = track_Item["album"]["name"]
                track_Data["song_Name"] = track_Item["name"]
                track_Data["song_Duration"] = track_Item["duration_ms"]
                track_Data["release_Date"] = track_Item["album"]["release_date"]
                track_Data["song_ID"] = track_Item["id"]
                track_Data["external_URL"] = track_Item["external_urls"]["spotify"]
                track_Data["images"] = track_Item["album"]["images"]
                
                search_Results["tracks"].append(track_Data)

        elif search_Type == "playlists":
            for playlist in range(len(search_Data[search_Type]["items"])):
                playlist_Item = search_Data[search_Type]["items"][playlist]

                playlist_Data = {}
                playlist_Data["name"] = playlist_Item["name"]
                playlist_Data["description"] = playlist_Item["description"]
                playlist_Data["external_URL"] = playlist_Item["external_urls"]["spotify"]
                playlist_Data["playlist_ID"] = playlist_Item["id"]
                playlist_Data["total_Tracks"] = playlist_Item["tracks"]["total"]
                playlist_Data["images"] = playlist_Item["images"]

                search_Results["playlists"].append(playlist_Data)

    return search_Results



def get_User_Top_Tracks(user_Unique_ID, entities_Limit=50, offset=0, time_Range="short_term"):
    """
    Получить список топ треков пользователя

    user_Unique_ID - Внутренний уникальный ID пользователя

    entities_Limit - Лимит выборки

    offset - Сдвиг выборки

    time_Range - Диапазон времени для выборки (short_term, medium_term, long_term)
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    user_Top = spotify_Api.get_User_Tops(user_Auth_Token, "tracks", entities_Limit, offset, time_Range)

    if not user_Top["total"] >= 1: #Проверка на наличие хотя бы одного элемента
        raise spotify_Exceptions.no_Tops_Data

    current_Timestamp = int(time.time())

    NEW_TopData = {
        "top_Info":{
            "entities_Limit":entities_Limit,
            "offset":offset,
            "time_Range":time_Range,
            "timestamp":current_Timestamp,
        },
        "items":[],
    }
    for item in range(user_Top["total"]):
        NEW_TopData["items"].append(
            {
                "prefix":" ",
                "name":user_Top["items"][item]["name"],
                "artists":user_Top["items"][item]["album"]["artists"][0]["name"],
                "preview_URL":user_Top["items"][item]["preview_url"],
                "URI":user_Top["items"][item]["uri"],
            }
        )

    database_User_Tracks = database_Manager.search_In_Database(user_Unique_ID, "users_TopTracks", "user_Unique_ID") #Для сравнения подгружаем старый кэш топа пользователя

    if database_User_Tracks: #Если у пользователя есть топ
        if time_Range == "short_term": #хахах, вот это костыли, вери найс гуд найс
            user_Tracks = database_User_Tracks[0][1]
        elif time_Range == "medium_term":
            user_Tracks = database_User_Tracks[0][2]
        elif time_Range == "long_term":
            user_Tracks = database_User_Tracks[0][3]
        
        if user_Tracks: #Проверяем есть ли старый кэш песен
            OLD_TopData = json.loads(user_Tracks) #Десериализуем строку в словарь

            if OLD_TopData["top_Info"]["time_Range"] == time_Range: #Если временной период выборки совпадает, то делаем сравнение
                OLD_URIS = [] #Отслеживание изменений происходит по ID, поэтому делаем список старой выборки
                for index in range(len(OLD_TopData["items"])):
                    OLD_URIS.append(OLD_TopData["items"][index]["URI"])

                NEW_URIS = [] #Список новой выборки
                for index in range(len(NEW_TopData["items"])):
                    NEW_URIS.append(NEW_TopData["items"][index]["URI"])
        
                for index_New in range(len(NEW_URIS)): #Сравниваем выборку по новой выборке
                    try:
                        old_Index = OLD_URIS.index(NEW_URIS[index_New])
                    except:
                        NEW_TopData["items"][index_New]["prefix"] = "● " #Если в старой выборке такой песни нет, ставим метку новой песни
                    else:
                        if old_Index < index_New:
                            NEW_TopData["items"][index_New]["prefix"] = "▼ " #Если песня опустилась ниже
                        elif old_Index > index_New:
                            NEW_TopData["items"][index_New]["prefix"] = "▲ " #Если песня поднялась выше
                        elif old_Index == index_New:
                            NEW_TopData["items"][index_New]["prefix"] = "  " #Если изменений не произошло

    return NEW_TopData



def get_User_Top_Artists(user_Unique_ID, entities_Limit=50, offset=0, time_Range="short_term"):
    """
    Получить список топ исполнителей пользователя

    user_Unique_ID - Внутренний уникальный ID пользователя

    entities_Limit - Лимит выборки

    offset - Сдвиг выборки

    time_Range - Диапазон времени для выборки (short_term, medium_term, long_term)
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    user_Top = spotify_Api.get_User_Tops(user_Auth_Token, "artists", entities_Limit, offset, time_Range)

    if not user_Top["total"] >= 1: #Проверка на наличие хотя бы одного элемента
        raise spotify_Exceptions.no_Tops_Data

    current_Timestamp = int(time.time())

    NEW_TopData = {
        "top_Info":{
            "entities_Limit":entities_Limit,
            "offset":offset,
            "time_Range":time_Range,
            "timestamp":current_Timestamp,
        },
        "items":[],
    }
    for artist in range(user_Top["total"]):
        NEW_TopData["items"].append(
            {
                "prefix":" ",
                "artist":user_Top["items"][artist]["name"],
                "followers":user_Top["items"][artist]["followers"]["total"],
                "URI":user_Top["items"][artist]["uri"],
            }
        )
    
    database_User_Artists = database_Manager.search_In_Database(user_Unique_ID, "users_TopArtists", "user_Unique_ID") #Для сравнения подгружаем старый кэш топа пользователя

    if database_User_Artists: #Если у пользователя есть топ
        if time_Range == "short_term": #хахах, вот это костыли, вери найс гуд найс
            user_Artists = database_User_Artists[0][1]
        elif time_Range == "medium_term":
            user_Artists = database_User_Artists[0][2]
        elif time_Range == "long_term":
            user_Artists = database_User_Artists[0][3]
        
        if user_Artists: #Проверяем есть ли старый кэш песен
            OLD_TopData = json.loads(user_Artists) #Десериализуем строку в словарь

            if OLD_TopData["top_Info"]["time_Range"] == time_Range: #Если временной период выборки совпадает, то делаем сравнение
                OLD_URIS = [] #Отслеживание изменений происходит по ID, поэтому делаем список старой выборки
                for index in range(len(OLD_TopData["items"])):
                    OLD_URIS.append(OLD_TopData["items"][index]["URI"])

                NEW_URIS = [] #Список новой выборки
                for index in range(len(NEW_TopData["items"])):
                    NEW_URIS.append(NEW_TopData["items"][index]["URI"])
        
                for index_New in range(len(NEW_URIS)): #Сравниваем выборку по новой выборке
                    try:
                        old_Index = OLD_URIS.index(NEW_URIS[index_New])
                    except:
                        NEW_TopData["items"][index_New]["prefix"] = "● " #Если в старой выборке такой песни нет, ставим метку новой песни
                    else:
                        if old_Index < index_New:
                            NEW_TopData["items"][index_New]["prefix"] = "▼ " #Если песня опустилась ниже
                        elif old_Index > index_New:
                            NEW_TopData["items"][index_New]["prefix"] = "▲ " #Если песня поднялась выше
                        elif old_Index == index_New:
                            NEW_TopData["items"][index_New]["prefix"] = "  " #Если изменений не произошло

    return NEW_TopData



def create_Top_Tracks_Playlist(user_Unique_ID, localization_Data, time_Range):
    """
    Создать плейлист с топ песнями пользователя

    user_Unique_ID - Внутренний уникальный ID пользователя
    """
    check_Token_Lifetime(user_Unique_ID)
    database_User_Data = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")
    user_Auth_Token = database_User_Data[0][4]
    user_Spotify_ID = database_User_Data[0][1]

    database_User_Tracks = database_Manager.search_In_Database(user_Unique_ID, "users_TopTracks", "user_Unique_ID")

    if database_User_Tracks: #Если у пользователя есть топ
        if time_Range == "short_term": #хахах, вот это костыли, вери найс гуд найс
            user_Tracks = database_User_Tracks[0][1]
        elif time_Range == "medium_term":
            user_Tracks = database_User_Tracks[0][2]
        elif time_Range == "long_term":
            user_Tracks = database_User_Tracks[0][3]

    top_Data = json.loads(user_Tracks) #Десериализуем строку в словарь

    playlist_Name = localization_Data["playlist_Name"].format(time_Range=localization_Data["playlist_TimeRange"])
    playlist_Name = time.strftime(playlist_Name)
    playlist_Description = localization_Data["playlist_Description"]
    new_Playlist_ID = spotify_Api.create_Playlist(user_Auth_Token, user_Spotify_ID, playlist_Name, playlist_Description)["id"]

    top_Tracks = []
    for track in range(len(top_Data["items"])):
        top_Tracks.append(top_Data["items"][track]["URI"])

    spotify_Api.add_Tracks_To_Playlist(user_Auth_Token, new_Playlist_ID, top_Tracks)

    return new_Playlist_ID



def create_MusicQuiz_Top_Tracks(user_Unique_ID, time_Range):
    """
    Создать музыкальную викторину из топ треков

    user_Unique_ID - Внутренний уникальный ID пользователя

    В случае ошибки возвращает исключение musicQuiz_Error_NoTracks (не хватает треков для викторины)

    time_Range - Диапазон времени для выборки (short_term, medium_term, long_term)
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    user_Top = spotify_Api.get_User_Tops(user_Auth_Token, "tracks", 50, 0, time_Range)

    if not user_Top["total"] >= 50: #Проверка на наличие хотя бы одного элемента
        raise spotify_Exceptions.no_Tops_Data

    top_Tracks = []
    for item in range(50): #Привести все элементы в человеческий вид
        if user_Top["items"][item]["preview_url"]: #Добавлять в список только песни с превью
            top_Tracks.append({
                "name":user_Top["items"][item]["name"],
                "artists":user_Top["items"][item]["album"]["artists"][0]["name"],
                "preview_URL":user_Top["items"][item]["preview_url"],
            })
    
    random.shuffle(top_Tracks) #Перемешать элементы топа

    right_Answers = []
    for item in range(10): #Выбрать из элементов топа 10 песен для игры
        right_Answers.append({
            "name":top_Tracks[item]["name"],
            "artists":top_Tracks[item]["artists"],
            "audio_URL":top_Tracks[item]["preview_URL"],
        })
        time.sleep(0.5)

        top_Tracks.pop(item) #Удалить их из выборки топа

    musicQuiz_Items = {}
    musicQuiz_Items["right_Answers"] = right_Answers
    musicQuiz_Items["other_Answers"] = top_Tracks

    if len(musicQuiz_Items["right_Answers"]) < 10 or len(musicQuiz_Items["other_Answers"]) < 20:
        raise spotify_Exceptions.musicQuiz_Error_NoTracks

    return musicQuiz_Items



def create_MusicQuiz_Liked_Songs(user_Unique_ID):
    """
    Создать музыкальную викторину из Liked Songs

    user_Unique_ID - Внутренний уникальный ID пользователя

    В случае ошибки возвращает исключение musicQuiz_Error_NoTracks (не хватает треков для викторины)
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]

    user_Data = spotify_Api.get_Saved_Tracks(user_Auth_Token)
    total_Iterations = math.ceil(user_Data["total"] / 50) #Поделить кол-во песен на запросы по 50 песен

    offset = 0
    liked_Tracks = []
    for user_Tracks in range(total_Iterations): #Выгрузить все песни пользователя
        user_Tracks = spotify_Api.get_Saved_Tracks(user_Auth_Token, 50, offset)

        offset += 50

        for track in range(len(user_Tracks["items"])): #Привести все элементы в человеческий вид
            if user_Tracks["items"][track]["track"]["preview_url"]: #Добавлять в список только песни с превью
                liked_Tracks.append({
                    "name":user_Tracks["items"][track]["track"]["name"],
                    "artists":user_Tracks["items"][track]["track"]["artists"][0]["name"],
                    "preview_URL":user_Tracks["items"][track]["track"]["preview_url"],
                })

    random.shuffle(liked_Tracks) #Перемешать элементы топа

    right_Answers = []
    for item in range(10): #Выбрать из элементов топа 10 песен для игры
        right_Answers.append({
            "name":liked_Tracks[item]["name"],
            "artists":liked_Tracks[item]["artists"],
            "audio_URL":liked_Tracks[item]["preview_URL"],
        })
        time.sleep(0.5)

        liked_Tracks.pop(item) #Удалить их из выборки топа

    musicQuiz_Items = {}
    musicQuiz_Items["right_Answers"] = right_Answers
    musicQuiz_Items["other_Answers"] = liked_Tracks

    if len(musicQuiz_Items["right_Answers"]) < 10 or len(musicQuiz_Items["other_Answers"]) < 20:
        raise spotify_Exceptions.musicQuiz_Error_NoTracks

    return musicQuiz_Items



def super_Shuffle(user_Unique_ID, localization_Data, tracks_Count=None):
    """
    Создать супер-шаффл из Liked Songs

    user_Unique_ID - Внутренний уникальный ID пользователя

    tracks_Count - Кол-во треков для супер-шаффла (не менее 100)
    """
    check_Token_Lifetime(user_Unique_ID)
    database_User_Data = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")
    user_Auth_Token = database_User_Data[0][4]
    user_Spotify_ID = database_User_Data[0][1]

    user_Data = spotify_Api.get_Saved_Tracks(user_Auth_Token)
    total_Iterations = math.ceil(user_Data["total"] / 50) #Поделить кол-во песен на запросы по 50 песен

    offset = 0
    liked_Tracks = []
    for user_Tracks in range(total_Iterations): #Выгрузить все песни пользователя
        user_Tracks = spotify_Api.get_Saved_Tracks(user_Auth_Token, 50, offset)

        offset += 50

        for track in range(len(user_Tracks["items"])): #Достать uri песни из всех данных
            liked_Tracks.append(user_Tracks["items"][track]["track"]["uri"])

    for user_Tracks in range(100): #Перемешать все песни 100 раз
        random.shuffle(liked_Tracks)

    playlist_Name = localization_Data["playlist_Name"]
    playlist_Name = time.strftime(playlist_Name)
    playlist_Description = localization_Data["playlist_Description"]
    new_Playlist_ID = spotify_Api.create_Playlist(user_Auth_Token, user_Spotify_ID, playlist_Name, playlist_Description)["id"] #Создать плейлист и получить его ID

    offset = 100
    if tracks_Count: #Если указано кол-во треков то вырезаем кол-во треков, если нет - вся выборка
        total_Iterations = math.ceil(tracks_Count / offset)
    else:
        total_Iterations = math.ceil(len(liked_Tracks) / offset)

    for user_Tracks in range(total_Iterations): #Закидываем все песни в плейлист
        playlist_Tracks = liked_Tracks[offset - 100:offset]
        spotify_Api.add_Tracks_To_Playlist(user_Auth_Token, new_Playlist_ID, playlist_Tracks)
        offset += 100

    return new_Playlist_ID