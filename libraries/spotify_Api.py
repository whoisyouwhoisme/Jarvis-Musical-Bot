import requests
import json
from libraries import spotify_Oauth
from spotify_Module import spotify_Exceptions



def return_Request_Headers(auth_Token):
    """
    The function returns the authorization header for the API
    """
    request_Headers = {
        "Accept":"application/json",
        "Content-Type":"application/json",
        "Authorization":"Bearer " + auth_Token,
    }

    return request_Headers



def get_Request(request_Link, headers, data=None):
    """
    The function performs a GET request, if successful, it returns a response

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    try:
        response = requests.get(request_Link, headers=headers, data=data, timeout=(3, 5))
        response.raise_for_status()

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.SSLError):
        raise spotify_Exceptions.http_Connection_Error

    except requests.exceptions.HTTPError:
        raise spotify_Exceptions.http_Error(response.status_code, response.reason)

    except:
        raise spotify_Exceptions.http_Unknown_Error

    else:
        return response



def put_Request(request_Link, headers, data=None):
    """
    The function performs a PUT request, if successful, it returns a response

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    try:
        response = requests.put(request_Link, headers=headers, data=data, timeout=(3, 5))
        response.raise_for_status()

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.SSLError):
        raise spotify_Exceptions.http_Connection_Error

    except requests.exceptions.HTTPError:
        raise spotify_Exceptions.http_Error(response.status_code, response.reason)

    except:
        raise spotify_Exceptions.http_Unknown_Error

    else:
        return response



def post_Request(request_Link, headers, data=None):
    """
    The function performs a POST request, if successful, it returns a response

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    try:
        response = requests.post(request_Link, headers=headers, data=data, timeout=(3, 5))
        response.raise_for_status()

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.SSLError):
        raise spotify_Exceptions.http_Connection_Error

    except requests.exceptions.HTTPError:
        raise spotify_Exceptions.http_Error(response.status_code, response.reason)

    except:
        raise spotify_Exceptions.http_Unknown_Error

    else:
        return response



def delete_Request(request_Link, headers, data=None):
    """
    The function performs a DELETE request, if successful, it returns a response

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    try:
        response = requests.delete(request_Link, headers=headers, data=data, timeout=(3, 5))
        response.raise_for_status()

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.SSLError):
        raise spotify_Exceptions.http_Connection_Error

    except requests.exceptions.HTTPError:
        raise spotify_Exceptions.http_Error(response.status_code, response.reason)

    except:
        raise spotify_Exceptions.http_Unknown_Error

    else:
        return response



def get_Current_Playback(auth_Token):
    """
    Get the current playback of the user, if successful, returns a response in JSON format

    auth_Token - Authorization token

    In case of an error, it returns the exceptions:
    no_Playback
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    request_Headers = return_Request_Headers(auth_Token)
    response = get_Request("https://api.spotify.com/v1/me/player", headers=request_Headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise spotify_Exceptions.no_Playback



def get_Saved_Tracks(auth_Token, market="US", limit=10, offset=0):
    """
    Get songs from the Liked Songs section, if successful, returns a response in JSON format

    auth_Token - Authorization key

    limit - Limit of songs (no more than 50)

    offset - Offset of the sample

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    request_Headers = return_Request_Headers(auth_Token)
    response = get_Request(f"https://api.spotify.com/v1/me/tracks?market={market}&limit={limit}&offset={offset}", headers=request_Headers)

    return response.json()



def create_Playlist(auth_Token, user_ID, playlist_Name, playlist_Description=None, public=False):
    """
    Create a playlist, if successful, returns a response in JSON format

    auth_Token - Authorization key

    user_ID - Unique user ID in Spotify

    playlist_Name - Playlist name

    playlist_Description - Playlist description (optional)

    public - Whether the playlist is public (by default, the playlist is private)

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    request_Headers = return_Request_Headers(auth_Token)
    request_Data = json.dumps({
        "name":playlist_Name,
        "description":playlist_Description,
        "public":public,
    })

    response = post_Request(f"https://api.spotify.com/v1/users/{user_ID}/playlists", headers=request_Headers, data=request_Data)

    return response.json()



def get_User_Playlists(auth_Token, entities_Limit=20, offset=0):
    """
    Get all playlists available to the user, if successful, returns a response in JSON format

    auth_Token - Authorization key

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    request_Headers = return_Request_Headers(auth_Token)

    response = get_Request(f"https://api.spotify.com/v1/me/playlists?limit={entities_Limit}&offset={offset}", headers=request_Headers)

    return response.json()



def get_Playlist_Tracks(auth_Token, playlist_Uri, entities_Limit=100, offset=0, market="US"):
    """
    Get tracks from the playlist, if successful, returns a response in JSON format

    auth_Token - Authorization key

    entities_Limit - Limit of songs (no more than 100)

    offset - Offset of the sample

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    request_Headers = return_Request_Headers(auth_Token)

    response = get_Request(f"https://api.spotify.com/v1/playlists/{playlist_Uri}/tracks?market={market}&fields=total%2Citems(track.name%2Ctrack.artists%2Ctrack.uri)&limit={entities_Limit}&offset={offset}", headers=request_Headers)

    return response.json()    



def add_Tracks_To_Playlist(auth_Token, playlist_ID, tracks_Uris):
    """
    Add tracks to the playlist, if successful, returns a response in JSON format

    auth_Token - Authorization key

    playlist_ID - Unique playlist ID in Spotify

    tracks_Uris - list of song IDs

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    request_Headers = return_Request_Headers(auth_Token)
    request_Data = json.dumps({
        "uris":tracks_Uris,
    })

    response = post_Request(f"https://api.spotify.com/v1/playlists/{playlist_ID}/tracks", headers=request_Headers, data=request_Data)

    return response.json()



def get_User_Tops(auth_Token, top_Type="tracks", entities_Limit=50, offset=0, time_Range="short_term"):
    """
    Get top, if successful, returns a response in JSON format

    auth_Token - Authorization key

    top_Type - Top type (tracks, artists)

    entities_Limit - Entities limit (no more than 50)

    offset - Offset of the sample

    time_Range - Time range to sample (short_term, medium_term, long_term)

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    request_Headers = return_Request_Headers(auth_Token)

    response = get_Request(f"https://api.spotify.com/v1/me/top/{top_Type}?time_range={time_Range}&limit={entities_Limit}&offset={offset}", headers=request_Headers)

    return response.json()



def get_Playlist_Info(auth_Token, playlist_ID):
    """
    Get information about the playlist, if successful, returns a response in JSON format

    auth_Token - Authorization key

    playlist_ID - Unique playlist ID in Spotify

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    request_Headers = return_Request_Headers(auth_Token)

    response = get_Request(f"https://api.spotify.com/v1/playlists/{playlist_ID}?fields=description%2Cname%2Cid%2Cimages%2Cexternal_urls%2Ctracks(total)", headers=request_Headers)

    return response.json()



def get_Album_Info(auth_Token, album_ID):
    """
    Get information about the album, if successful, returns a response in JSON format

    auth_Token - Authorization key

    album_ID - Unique album ID on Spotify

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    request_Headers = return_Request_Headers(auth_Token)

    response = get_Request(f"https://api.spotify.com/v1/albums/{album_ID}", headers=request_Headers)

    return response.json()



def get_Artist_Info(auth_Token, artist_ID):
    """
    Get information about the executor, if successful, returns a response in JSON format

    auth_Token - Authorization key

    artist_ID - Unique artist ID on Spotify

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    request_Headers = return_Request_Headers(auth_Token)

    response = get_Request(f"https://api.spotify.com/v1/artists/{artist_ID}", headers=request_Headers)

    return response.json()



def get_Several_Artists_Info(auth_Token, artists_IDs):
    """
    Get information about MULTIPLE executors, if successful, returns a response in JSON format

    auth_Token - Authorization key

    artist_ID - LIST of Unique Artist IDs on Spotify

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    request_Headers = return_Request_Headers(auth_Token)

    artists_IDs_String = ",".join(artists_IDs)

    response = get_Request(f"https://api.spotify.com/v1/artists?ids={artists_IDs_String}", headers=request_Headers)

    return response.json()




def get_User_Devices(auth_Token):
    """ 
    Get information about the user's available devices, if successful, returns a response in JSON format

    auth_Token - Authorization key

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    request_Headers = return_Request_Headers(auth_Token)

    response = get_Request("https://api.spotify.com/v1/me/player/devices", headers=request_Headers)

    return response.json()



def search_Item(auth_Token, search_Query, search_Types="track", limit=5, offset=0):
    """
    Search Spotify, if successful, returns a JSON response

    auth_Token - Authorization key

    search_Query - Search query

    search_Types - Types for search, artist, album, track

    limit - Limit of search items

    offset - Offset of the search items

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    request_Headers = return_Request_Headers(auth_Token)

    response = get_Request(f"https://api.spotify.com/v1/search?q={search_Query}&type={search_Types}&limit={limit}&offset={offset}", headers=request_Headers)

    return response.json()



def start_Playback(auth_Token, playback_Context=None, playback_Uris=None):
    """
    Start new playback.

    auth_Token - Authorization key

    playback_Context - Context for playback (playlist, artist)

    OR

    playback_Uris - List of Spotify track URIs

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    request_Headers = return_Request_Headers(auth_Token)
    if playback_Context:
        request_Data = json.dumps({
            "context_uri":playback_Context,
        })
    elif playback_Uris:
        request_Data = json.dumps({
            "uris":playback_Uris,
        })        

    response = put_Request("https://api.spotify.com/v1/me/player/play", headers=request_Headers, data=request_Data)

    return response



def add_Track_To_Queue(auth_Token, track_Uri):
    """
    Add a track to the user's play queue

    auth_Token - Authorization key

    track_Uri - URI of the song

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    request_Headers = return_Request_Headers(auth_Token)

    response = post_Request(f"https://api.spotify.com/v1/me/player/queue?uri={track_Uri}", headers=request_Headers)

    return response



def get_User_Profile(auth_Token):
    """
    Get user profile in Spotify, if successful, returns a JSON response

    auth_Token - Spotify API access token

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    request_Headers = return_Request_Headers(auth_Token)

    response = get_Request("https://api.spotify.com/v1/me", headers=request_Headers)

    return response.json()



def delete_Playlist_Tracks(auth_Token, playlist_ID, playlist_Tracks):
    """
    Removes tracks from the playlist, returns HTTP response code

    auth_Token - Spotify API access token

    playlist_ID - Unique playlist ID in Spotify

    playlist_Tracks - LIST of Spotify track URIs

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    request_Headers = return_Request_Headers(auth_Token)

    tracks_Data = {"tracks":[]}
    for track in range(len(playlist_Tracks)):
        tracks_Data["tracks"].append({"uri":playlist_Tracks[track],"positions":[0]})

    request_Data = json.dumps(tracks_Data)

    response = delete_Request(f"https://api.spotify.com/v1/playlists/{playlist_ID}/tracks", headers=request_Headers, data=request_Data)

    return response.status_code



def delete_Liked_Tracks(auth_Token, tracks_ID):
    """
    Removes tracks from the Favorite tracks section, returns an HTTP response code

    auth_Token - Spotify API access token

    tracks_ID - LIST of Spotify track URIs

    In case of an error, it returns the exceptions:
    http_Connection_Error
    http_Error(response code, reason)
    http_Unknown_Error
    """
    request_Headers = return_Request_Headers(auth_Token)

    request_Data = json.dumps(tracks_ID)

    response = delete_Request("https://api.spotify.com/v1/me/tracks", headers=request_Headers, data=request_Data)

    return response.status_code