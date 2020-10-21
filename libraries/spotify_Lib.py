import requests
import json
from libraries import spotify_Oauth
from spotify_Module import spotify_Exceptions



def return_Request_Headers(auth_Token):
    """
    Функция возвращает заголовок для API
    """
    request_Headers = {
        "Accept":"application/json",
        "Content-Type":"application/json",
        "Authorization":"Bearer " + auth_Token,
    }

    return request_Headers



def get_Request(request_Link, headers, data=None):
    """
    Функция выполняет GET запрос, в случае успеха возвращает ответ

    В случае ошибки, возвращает исключения oauth_Connection_Error, oauth_Http_Error, oauth_Unknown_Error
    """
    try:
        response = requests.get(request_Link, headers=headers, data=data, timeout=(3, 5))
        response.raise_for_status()

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.SSLError):
        raise spotify_Exceptions.oauth_Connection_Error

    except requests.exceptions.HTTPError:
        raise spotify_Exceptions.oauth_Http_Error(response.status_code, response.reason)

    except:
        raise spotify_Exceptions.oauth_Unknown_Error

    else:
        return response



def put_Request(request_Link, headers, data=None):
    """
    Функция выполняет PUT запрос, в случае успеха возвращает ответ

    В случае ошибки, возвращает исключения oauth_Connection_Error, oauth_Http_Error, oauth_Unknown_Error
    """
    try:
        response = requests.put(request_Link, headers=headers, data=data, timeout=(3, 5))
        response.raise_for_status()

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.SSLError):
        raise spotify_Exceptions.oauth_Connection_Error

    except requests.exceptions.HTTPError:
        raise spotify_Exceptions.oauth_Http_Error(response.status_code, response.reason)

    except:
        raise spotify_Exceptions.oauth_Unknown_Error

    else:
        return response



def post_Request(request_Link, headers, data=None):
    """
    Функция выполняет POST запрос, в случае успеха возвращает ответ

    В случае ошибки, возвращает исключения oauth_Connection_Error, oauth_Http_Error, oauth_Unknown_Error
    """
    try:
        response = requests.post(request_Link, headers=headers, data=data, timeout=(3, 5))
        response.raise_for_status()

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.SSLError):
        raise spotify_Exceptions.oauth_Connection_Error

    except requests.exceptions.HTTPError:
        raise spotify_Exceptions.oauth_Http_Error(response.status_code, response.reason)

    except:
        raise spotify_Exceptions.oauth_Unknown_Error

    else:
        return response



def get_Current_Playback(auth_Token):
    """
    Получить текущее проигрывание пользователя, в случае успеха возвращает ответ в формате json

    В случае ошибки возвращает исключения no_Playback, oauth_Connection_Error, oauth_Http_Error, oauth_Unknown_Error

    auth_Token - Ключ авторизации
    """
    request_Headers = return_Request_Headers(auth_Token)
    response = get_Request("https://api.spotify.com/v1/me/player", headers=request_Headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise spotify_Exceptions.no_Playback



def get_Saved_Tracks(auth_Token, limit=10, offset=0):
    """
    Получить песни из раздела Liked Songs, в случае успеха возвращает ответ в формате json

    В случае ошибки возвращает исключения oauth_Connection_Error, oauth_Http_Error, oauth_Unknown_Error

    auth_Token - Ключ авторизации

    limit - Лимит песен (не более 50)

    offset - Смещение выборки
    """
    request_Headers = return_Request_Headers(auth_Token)
    response = get_Request(f"https://api.spotify.com/v1/me/tracks?limit={limit}&offset={offset}", headers=request_Headers)

    return response.json()



def create_Playlist(auth_Token, user_ID, playlist_Name, playlist_Description=None, public=False):
    """
    Создать плейлист, в случае успеха возвращает ответ в формате json

    В случае ошибки возвращает исключения oauth_Connection_Error, oauth_Http_Error, oauth_Unknown_Error

    auth_Token - Ключ авторизации

    user_ID - Уникальный ID пользователя в Spotify

    playlist_Name - Название плейлиста

    playlist_Description - Описание плейлиста (необязательный параметр)

    public - Публичный ли плейлист (по умолчанию - плейлист закрытый)
    """
    request_Headers = return_Request_Headers(auth_Token)
    request_Data = json.dumps({
        "name":playlist_Name,
        "description":playlist_Description,
        "public":public,
    })

    response = post_Request(f"https://api.spotify.com/v1/users/{user_ID}/playlists", headers=request_Headers, data=request_Data)

    return response.json()



def add_Tracks_To_Playlist(auth_Token, playlist_ID, tracks_Uris):
    """
    Добавить треки в плейлист, в случае успеха возвращает ответ в формате json

    В случае ошибки возвращает исключения oauth_Connection_Error, oauth_Http_Error, oauth_Unknown_Error

    auth_Token - Ключ авторизации

    playlist_ID - Уникальный ID плейлиста в Spotify

    tracks_Uris - список идентификаторов песен
    """
    request_Headers = return_Request_Headers(auth_Token)
    request_Data = json.dumps({
        "uris":tracks_Uris,
    })

    response = post_Request(f"https://api.spotify.com/v1/playlists/{playlist_ID}/tracks", headers=request_Headers, data=request_Data)

    return response.json()



def get_User_Tops(auth_Token, top_Type="tracks", entities_Limit=50, offset=0, time_Range="short_term"):
    """
    Получить топ, в случае успеха возвращает ответ в формате json

    В случае ошибки возвращает исключения oauth_Connection_Error, oauth_Http_Error, oauth_Unknown_Error

    auth_Token - Ключ авторизации

    top_Type - Тип топа (tracks, artists)

    entities_Limit - Лимит объектов (не более 50)

    offset - Смещение выборки

    time_Range - Диапазон времени для выборки (short_term, medium_term, long_term)
    """
    request_Headers = return_Request_Headers(auth_Token)

    response = get_Request(f"https://api.spotify.com/v1/me/top/{top_Type}?time_range={time_Range}&limit={entities_Limit}&offset={offset}", headers=request_Headers)

    return response.json()



def get_Playlist_Info(auth_Token, playlist_ID):
    """
    Получить информацию о плейлисте, в случае успеха возвращает ответ в формате json

    В случае ошибки возвращает исключения oauth_Connection_Error, oauth_Http_Error, oauth_Unknown_Error

    auth_Token - Ключ авторизации

    playlist_ID - Уникальный ID плейлиста в Spotify
    """
    request_Headers = return_Request_Headers(auth_Token)

    response = get_Request(f"https://api.spotify.com/v1/playlists/{playlist_ID}?fields=description%2Cname%2Cid%2Cimages%2Cexternal_urls%2Ctracks(total)", headers=request_Headers)

    return response.json()



def get_User_Devices(auth_Token):
    """ 
    Получить информацию о доступных устройствах пользователя, в случае успеха возвращает ответ в формате json

    В случае ошибки возвращает исключения oauth_Connection_Error, oauth_Http_Error, oauth_Unknown_Error

    auth_Token - Ключ авторизации
    """
    request_Headers = return_Request_Headers(auth_Token)

    response = get_Request(f"https://api.spotify.com/v1/me/player/devices", headers=request_Headers)

    return response.json()



def start_Playback(auth_Token, device_ID, playback_Context):
    """
    Запустить новое проигрывание.

    В случае ошибки возвращает исключения oauth_Connection_Error, oauth_Http_Error, oauth_Unknown_Error

    auth_Token - Ключ авторизации

    device_ID - ID устройства пользователя

    playback_Context - Что требуется проигрывать (например spotify:playlist:0soXLPoBV9LGgpwCZOvVi5)
    """
    request_Headers = return_Request_Headers(auth_Token)
    request_Data = json.dumps({
        "context_uri":playback_Context,
    })

    response = put_Request("https://api.spotify.com/v1/me/player/play", headers=request_Headers, data=request_Data)

    return response