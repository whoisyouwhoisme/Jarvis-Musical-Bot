import math
import time
import json
import random
from libraries import database_Manager
from libraries import spotify_Lib
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

    В случае ошибки возвращает исключение no_Data (не хватает мета-данных)

    user_Unique_ID - Внутренний уникальный ID пользователя
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    user_Playback = spotify_Lib.get_Current_Playback(user_Auth_Token)

    try:
        playback_Data = {"artists":[]}

        playback_Data["device_Info"] = {
            "device_ID":user_Playback["device"]["id"],
            "device_Name":user_Playback["device"]["name"],
            "device_Type":user_Playback["device"]["type"]
        }

        for artist in range(len(user_Playback["item"]["artists"])):
            playback_Data["artists"] += [user_Playback["item"]["artists"][artist]["name"]]

        playback_Data["album_Name"] = user_Playback["item"]["album"]["name"]
        playback_Data["song_Name"] = user_Playback["item"]["name"]
        playback_Data["song_Duration"] = user_Playback["item"]["duration_ms"]
        playback_Data["song_URI"] = user_Playback["item"]["uri"]
        playback_Data["external_URL"] = user_Playback["item"]["external_urls"]["spotify"]
        playback_Data["song_Cover_URL"] = user_Playback["item"]["album"]["images"][1]["url"]

        search_Keywords = ", ".join(playback_Data["artists"]) + " " + playback_Data["song_Name"]
        search_Result = youtube_Lib.search_Youtube(search_Keywords) #Поиск Ютуб клипа для песни

        if search_Result["items"]: #Если песня найдена
            first_Result_ID = search_Result["items"][0]["id"]["videoId"]
            playback_Data["youtube_URL"] = "https://www.youtube.com/watch?v=" + first_Result_ID
        else:
            playback_Data["youtube_URL"] = ""

    except:
        raise spotify_Exceptions.no_Data
    
    else:
        return playback_Data



def start_Playback(user_Unique_ID, playback_Context):
    """
    Начинает воспроизведение контента, в случае успеха возвращает True

    В случае ошибки возвращает исключения:
    no_ActiveDevices - Нет активных устройств
    premium_Required - Требуется премиум-подписка

    user_Unique_ID - Внутренний уникальный ID пользователя

    playback_Context - Контекст для проигрывания (плейлист, исполнитель)
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    user_Devices = spotify_Lib.get_User_Devices(user_Auth_Token)

    if user_Devices["devices"]: #Проверка наличия активного устройства
        latest_User_Device = user_Devices["devices"][0]["id"]
    else:
        raise spotify_Exceptions.no_ActiveDevices

    try:
        spotify_Lib.start_Playback(user_Auth_Token, latest_User_Device, playback_Context)

    except spotify_Exceptions.oauth_Http_Error as error:
        if error.http_Code == 404:
            raise spotify_Exceptions.no_ActiveDevices
        
        elif error.http_Code == 403:
            raise spotify_Exceptions.premium_Required

    else:
        return True



def get_Playlist_Data(user_Unique_ID, playlist_ID):
    """
    Найти в YouTube клип для текущего воспроизведения, возвращает словарь

    user_Unique_ID - Внутренний уникальный ID пользователя

    playlist_ID - Уникальный ID плейлиста в Spotify
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    playlist_Info = spotify_Lib.get_Playlist_Info(user_Auth_Token, playlist_ID)

    playlist_Data = {}
    playlist_Data["name"] = playlist_Info["name"]
    playlist_Data["description"] = playlist_Info["description"]
    playlist_Data["external_URL"] = playlist_Info["external_urls"]["spotify"]
    playlist_Data["playlist_ID"] = "spotify:playlist:" + playlist_Info["id"]
    playlist_Data["total_Tracks"] = playlist_Info["tracks"]["total"]
    playlist_Data["image_URL"] = playlist_Info["images"][1]["url"]

    return playlist_Data



def check_User_Liked_Songs(user_Unique_ID, minimum_Count):
    """
    Проверяет есть ли у пользователя минимальное кол-во Liked Songs, в случае успеха возвращает True

    В случае ошибки возвращает исключение no_Tracks (треков не хватает)

    user_Unique_ID - Внутренний уникальный ID пользователя

    minimum_Count - Кол-во треков
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    user_Data = spotify_Lib.get_Saved_Tracks(user_Auth_Token)

    if user_Data["total"] >= minimum_Count:
        return True
    else:
        raise spotify_Exceptions.no_Tracks



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
    user_Top = spotify_Lib.get_User_Tops(user_Auth_Token, "tracks", entities_Limit, offset, time_Range)

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
    for item in range(entities_Limit):
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
    user_Top = spotify_Lib.get_User_Tops(user_Auth_Token, "artists", entities_Limit, offset, time_Range)

    if not user_Top["total"] >= 1: #Проверка на наличие хотя бы одного элемента
        raise spotify_Exceptions.no_Tops_Data

    current_Timestamp = int(time.time())

    top_Artists = {
        "top_Info":{
            "entities_Limit":entities_Limit,
            "offset":offset,
            "time_Range":time_Range,
            "timestamp":current_Timestamp,
        },
        "items":[],
    }
    for artist in range(entities_Limit):
        top_Artists["items"].append(
            {
                "artist":user_Top["items"][artist]["name"],
                "followers":user_Top["items"][artist]["followers"]["total"],
                "URI":user_Top["items"][artist]["uri"],
            }
        )

    return top_Artists



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
    new_Playlist_ID = spotify_Lib.create_Playlist(user_Auth_Token, user_Spotify_ID, playlist_Name, playlist_Description)["id"]

    top_Tracks = []
    for track in range(len(top_Data["items"])):
        top_Tracks.append(top_Data["items"][track]["URI"])

    spotify_Lib.add_Tracks_To_Playlist(user_Auth_Token, new_Playlist_ID, top_Tracks)

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
    user_Top = spotify_Lib.get_User_Tops(user_Auth_Token, "tracks", 50, 0, time_Range)

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

    user_Data = spotify_Lib.get_Saved_Tracks(user_Auth_Token)
    total_Iterations = math.ceil(user_Data["total"] / 50) #Поделить кол-во песен на запросы по 50 песен

    offset = 0
    liked_Tracks = []
    for user_Tracks in range(total_Iterations): #Выгрузить все песни пользователя
        user_Tracks = spotify_Lib.get_Saved_Tracks(user_Auth_Token, 50, offset)

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

    user_Data = spotify_Lib.get_Saved_Tracks(user_Auth_Token)
    total_Iterations = math.ceil(user_Data["total"] / 50) #Поделить кол-во песен на запросы по 50 песен

    offset = 0
    liked_Tracks = []
    for user_Tracks in range(total_Iterations): #Выгрузить все песни пользователя
        user_Tracks = spotify_Lib.get_Saved_Tracks(user_Auth_Token, 50, offset)

        offset += 50

        for track in range(len(user_Tracks["items"])): #Достать uri песни из всех данных
            liked_Tracks.append(user_Tracks["items"][track]["track"]["uri"])

    for user_Tracks in range(500): #Перемешать все песни 500 раз
        random.shuffle(liked_Tracks)

    playlist_Name = localization_Data["playlist_Name"]
    playlist_Name = time.strftime(playlist_Name)
    playlist_Description = localization_Data["playlist_Description"]
    new_Playlist_ID = spotify_Lib.create_Playlist(user_Auth_Token, user_Spotify_ID, playlist_Name, playlist_Description)["id"] #Создать плейлист и получить его ID

    offset = 100
    if tracks_Count: #Если указано кол-во треков то вырезаем кол-во треков, если нет - вся выборка
        total_Iterations = math.ceil(tracks_Count / offset)
    else:
        total_Iterations = math.ceil(len(liked_Tracks) / offset)

    for user_Tracks in range(total_Iterations): #Закидываем все песни в плейлист
        playlist_Tracks = liked_Tracks[offset - 100:offset]
        spotify_Lib.add_Tracks_To_Playlist(user_Auth_Token, new_Playlist_ID, playlist_Tracks)
        offset += 100

    return new_Playlist_ID