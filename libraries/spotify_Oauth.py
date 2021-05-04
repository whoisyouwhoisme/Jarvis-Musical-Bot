import requests
import json
import time
from spotify_Module import bot_Sender
from spotify_Module import spotify_Exceptions
from libraries import spotify_Api
from libraries import database_Manager
from base64 import b64encode

with open("bot_Keys.json") as bot_Keys_File:
    bot_Keys = json.load(bot_Keys_File)

client_ID = bot_Keys["spotify"]["client_ID"]
client_Secret = bot_Keys["spotify"]["client_Secret"]

api_Scopes = [
        "user-read-playback-state", 
        "user-read-currently-playing", 
        "user-modify-playback-state", 
        "streaming user-library-read", 
        "user-read-recently-played", 
        "user-top-read", 
        "playlist-modify-private", 
        "user-read-private", 
        "playlist-read-private", 
        "playlist-modify-public", 
        "playlist-modify-private", 
        "user-library-modify"
    ]

spotify_Redirect_URI = bot_Keys["spotify"]["redirect_URI"]



def generate_Auth_Link(user_Unique_ID):
    """
    Generating a link for user authorization, returns a URL string

    user_Unique_ID - Unique user ID
    """
    auth_Scopes = "+".join(api_Scopes)

    spotify_Auth_Link = f"https://accounts.spotify.com/authorize?client_id={client_ID}&redirect_uri={spotify_Redirect_URI}&response_type=code&scope={auth_Scopes}&state={user_Unique_ID}"

    return spotify_Auth_Link



def request_Access_Tokens(user_Auth_Code):
    """
    Receiving authorization and update tokens, if successful, returns a response in JSON format

    user_Auth_Code - User authorization code

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    api_Access_Link = "https://accounts.spotify.com/api/token"

    auth_Session = requests.Session()

    header_String = str.encode(client_ID + ":" + client_Secret)
    base64_Header_String = b64encode(header_String).decode()

    auth_Headers = {
        "Authorization":"Basic " + base64_Header_String,
    }

    auth_Payload = {
        "grant_type":"authorization_code",
        "code":user_Auth_Code,
        "redirect_uri":spotify_Redirect_URI,
    }

    try:
        response = auth_Session.post(api_Access_Link, headers=auth_Headers, data=auth_Payload, timeout=(3, 5))
        response.raise_for_status()
        
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.SSLError):
        raise spotify_Exceptions.http_Connection_Error

    except requests.exceptions.HTTPError:
        raise spotify_Exceptions.http_Error(response.status_code, response.reason)

    except:
        raise spotify_Exceptions.http_Unknown_Error

    else:
        return response.json()



def request_Refreshed_Token(user_Refresh_Token):
    """
    Request to update the access token, if successful, returns a response in json format

    user_Refresh_Token - Token to refresh the API access token

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    api_Access_Link = "https://accounts.spotify.com/api/token"

    auth_Session = requests.Session()

    header_String = str.encode(client_ID + ":" + client_Secret)
    base64_Header_String = b64encode(header_String).decode()

    auth_Headers = {
        "Authorization":"Basic " + base64_Header_String,
    }

    auth_Payload = {
        "grant_type":"refresh_token",
        "refresh_token":user_Refresh_Token,
    }
    
    try:
        response = auth_Session.post(api_Access_Link, headers=auth_Headers, data=auth_Payload, timeout=(3, 5))
        response.raise_for_status()
        
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.SSLError):
        raise spotify_Exceptions.http_Connection_Error

    except requests.exceptions.HTTPError:
        raise spotify_Exceptions.http_Error(response.status_code, response.reason)

    except:
        raise spotify_Exceptions.http_Unknown_Error

    else:
        return response.json()



def refresh_Access_Token(user_Unique_ID):
    """
    Retrieving the updated access token and writing it to the database

    user_Unique_ID - Unique user ID

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    get_Refresh_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][5]

    request_Data = request_Refreshed_Token(get_Refresh_Token)
    refreshed_Token = request_Data["access_token"]
    refresh_Timestamp = int(time.time())
    database_Manager.write_Refreshed_Token(user_Unique_ID, refreshed_Token, refresh_Timestamp)



def auth_User(user_Auth_Code, user_Unique_ID):
    """
    User authorization and writing all data to the database

    user_Auth_Code - Spotify authorization code

    user_Unique_ID - Unique user ID

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    payload_Data = request_Access_Tokens(user_Auth_Code)
    user_Profile = spotify_Api.get_User_Profile(payload_Data["access_token"])

    user_Telegram_ID = database_Manager.search_In_Database(user_Unique_ID, "bot_Users", "user_Unique_ID")[0][0]
    user_Language = database_Manager.get_User_Language(user_Telegram_ID)

    auth_Timestamp = int(time.time())

    database_Manager.register_Spotify(user_Unique_ID, user_Profile["id"], user_Profile["display_name"], user_Auth_Code, payload_Data["access_token"], payload_Data["refresh_token"], auth_Timestamp, auth_Timestamp)
    database_Manager.write_User_Position(user_Telegram_ID, "main_Menu")
    
    bot_Sender.auth_Complete(user_Telegram_ID, user_Profile["display_name"], language_Name=user_Language)
    bot_Sender.controls_Main_Menu(user_Telegram_ID, language_Name=user_Language)