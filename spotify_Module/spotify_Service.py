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
    Check if the token is still alive, if the token is dead, update it

    user_Unique_ID - Internal unique user ID
    """
    current_Timestamp = int(time.time())
    last_Refresh_Timestamp = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][7]

    if (current_Timestamp - (last_Refresh_Timestamp - 60)) > 3600:
        spotify_Oauth.refresh_Access_Token(user_Unique_ID)



def get_Current_Playing(user_Unique_ID):
    """
    Get the current playback of the user, if successful, returns a dictionary

    Returns exceptions on error:
    no_Playback - nothing plays
    no_Data - not enough meta data
    private_Session_Enabled - private session is activated

    user_Unique_ID - Internal unique user ID
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
        try: #A crutch to bypass search quotas. Someday do the authorization through Google account...
            search_Result = youtube_Lib.search_Youtube(search_Keywords) #Search YouTube clip for song
        
        except:
            playback_Data["youtube_URL"] = ""
        
        else:
            if search_Result["items"]: #If a song clip is found
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
    Get the current user context

    Returns exceptions on error:
    no_Playback - nothing plays
    no_Playing_Context - no active context
    private_Session_Enabled - private session is activated

    user_Unique_ID - Internal unique user ID
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    user_Playback = spotify_Api.get_Current_Playback(user_Auth_Token)

    if user_Playback["device"]["is_private_session"]:
        raise spotify_Exceptions.private_Session_Enabled

    playback_Data = {}

    if user_Playback["context"]:
        playback_Data["context_URI"] = user_Playback["context"]["uri"]
        playback_Data["context_Type"] = user_Playback["context"]["type"]

        return playback_Data
    else:
        raise spotify_Exceptions.no_Playing_Context




def start_Playback(user_Unique_ID, playback_Context=None, playback_Uris=None):
    """
    Starts playing content, returns True on success

    Returns exceptions on error:
    no_ActiveDevices - No active devices
    premium_Required - Premium subscription required

    user_Unique_ID - Internal unique user ID

    playback_Context - Context for playback (playlist, artist)

    OR

    playback_Uris - List of Spotify track URIs
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    user_Devices = spotify_Api.get_User_Devices(user_Auth_Token)

    if not user_Devices["devices"]: #Checking for an active device
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
    Add a track to the user's play queue

    Returns exceptions on error:
    no_ActiveDevices - No active devices
    premium_Required - Premium subscription required

    user_Unique_ID - Internal unique user ID

    track_Uri - URI of the song
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
    Returns information about a playlist by ID

    user_Unique_ID - Internal unique user ID

    playlist_ID - Unique playlist ID in Spotify
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
    Returns information about an album by ID

    user_Unique_ID - Internal unique user ID

    album_ID - Unique playlist ID in Spotify
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
    Returns information about the artist by ID

    user_Unique_ID - Internal unique user ID

    artist_ID - Unique artist ID on Spotify
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
    Checks if the user has a minimum number of Liked Songs, if successful, returns True

    Returns the exception no_Tracks (there are not enough tracks) in case of an error

    user_Unique_ID - Internal unique user ID

    minimum_Count - Number of tracks
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    user_Country = spotify_Api.get_User_Profile(user_Auth_Token)["country"]
    user_Data = spotify_Api.get_Saved_Tracks(user_Auth_Token, market=user_Country)

    if user_Data["total"] >= minimum_Count:
        return True
    else:
        raise spotify_Exceptions.no_Tracks



def search_Item(user_Unique_ID, search_Query, search_Types="track", limit=5, offset=0):
    """
    Search in Spotify

    user_Unique_ID - Internal unique user ID

    search_Query - Search query

    search_Types - Types for search, artist, album, track

    limit - Limit of search items

    offset - Offset of the search items
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
                track_Data["preview_URL"] = track_Item["preview_url"]
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



def get_User_Blocked_Tracks(user_Unique_ID):
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]

    user_Country = spotify_Api.get_User_Profile(user_Auth_Token)["country"]
    user_Data = spotify_Api.get_Saved_Tracks(user_Auth_Token, market=user_Country)

    if user_Data["total"] == 0:
        raise spotify_Exceptions.no_Tracks

    total_Iterations = math.ceil(user_Data["total"] / 50) #Divide the number of songs for requests by 50 songs

    creation_Timestamp = int(time.time())

    offset = 0
    NEW_Blocked_Tracks = {
        "user_Country":user_Country,
        "blocked_Count":0,
        "tracks_Count":user_Data["total"],
        "creation_Timestamp":creation_Timestamp,
        "comparsion_Timestamp":None,
        "items":[]
        }
    
    for user_Tracks in range(total_Iterations): #Upload all user songs
        user_Tracks = spotify_Api.get_Saved_Tracks(user_Auth_Token, market=user_Country, limit=50, offset=offset)

        offset += 50

        for track in range(len(user_Tracks["items"])): #Loop over all songs in the current iteration
                if not user_Tracks["items"][track]["track"]["is_playable"]:
                    NEW_Blocked_Tracks["items"].append({
                            "prefix":" ",
                            "artists":user_Tracks["items"][track]["track"]["artists"][0]["name"],
                            "name":user_Tracks["items"][track]["track"]["name"],
                            "URI":user_Tracks["items"][track]["track"]["uri"]
                        })
    
    NEW_Blocked_Tracks["blocked_Count"] = len(NEW_Blocked_Tracks["items"])

    database_Blocked_Tracks = database_Manager.search_In_Database(user_Unique_ID, "users_BlockedTracks", "user_Unique_ID")

    if database_Blocked_Tracks:
        OLD_Blocked_Tracks = json.loads(database_Blocked_Tracks[0][1])

        NEW_Blocked_Tracks["comparsion_Timestamp"] = OLD_Blocked_Tracks["creation_Timestamp"]

        OLD_URIS = [] #Changes are tracked by ID, so we make a list of the old selection
        for index in range(len(OLD_Blocked_Tracks["items"])):
            OLD_URIS.append(OLD_Blocked_Tracks["items"][index]["URI"])

        NEW_URIS = [] #New selection list
        for index in range(len(NEW_Blocked_Tracks["items"])):
            NEW_URIS.append(NEW_Blocked_Tracks["items"][index]["URI"])

        for new_Item in range(len(NEW_URIS)):
            if not NEW_URIS[new_Item] in OLD_URIS:
                NEW_Blocked_Tracks["items"][new_Item]["prefix"] = "● "

    return NEW_Blocked_Tracks



def get_User_Top_Tracks(user_Unique_ID, entities_Limit=50, offset=0, time_Range="short_term"):
    """
    Get a list of the user's top tracks

    user_Unique_ID - Internal unique user ID

    entities_Limit - Selection limit

    offset - Offset of the sample

    time_Range - Time range to sample (short_term, medium_term, long_term)
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    user_Top = spotify_Api.get_User_Tops(user_Auth_Token, "tracks", entities_Limit, offset, time_Range)

    if not user_Top["total"] >= 1: #Checking for the presence of at least one element
        raise spotify_Exceptions.no_Tops_Data

    creation_Timestamp = int(time.time())

    NEW_TopData = {
        "entities_Limit":entities_Limit,
        "offset":offset,
        "time_Range":time_Range,
        "creation_Timestamp":creation_Timestamp,
        "comparsion_Timestamp":None,
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

    database_User_Tracks = database_Manager.search_In_Database(user_Unique_ID, "users_TopTracks", "user_Unique_ID") #For comparison, we load the old cache of the user's top

    if database_User_Tracks:
        if time_Range == "short_term":
            user_Tracks = database_User_Tracks[0][1]
        elif time_Range == "medium_term":
            user_Tracks = database_User_Tracks[0][2]
        elif time_Range == "long_term":
            user_Tracks = database_User_Tracks[0][3]
        
        if user_Tracks: #Check if there is an old cache of songs
            OLD_TopData = json.loads(user_Tracks) #Deserialize the string into a dictionary

            if OLD_TopData["time_Range"] == time_Range: #If the sample time period is the same, then we make a comparison
                NEW_TopData["comparsion_Timestamp"] = OLD_TopData["creation_Timestamp"]

                OLD_URIS = [] #Changes are tracked by ID, so we make a list of the old selection
                for index in range(len(OLD_TopData["items"])):
                    OLD_URIS.append(OLD_TopData["items"][index]["URI"])

                NEW_URIS = [] #New selection list
                for index in range(len(NEW_TopData["items"])):
                    NEW_URIS.append(NEW_TopData["items"][index]["URI"])
        
                for index_New in range(len(NEW_URIS)): #Comparing the sample for the new sample
                    try:
                        old_Index = OLD_URIS.index(NEW_URIS[index_New])
                    except:
                        NEW_TopData["items"][index_New]["prefix"] = "● " #If there is no such song in the old sample, we mark the new song
                    else:
                        if old_Index < index_New:
                            index_Offset = str(index_New - old_Index)
                            NEW_TopData["items"][index_New]["prefix"] = f" ▼ +{index_Offset}" #If the song went down
                        elif old_Index > index_New:
                            index_Offset = str(index_New - old_Index)
                            NEW_TopData["items"][index_New]["prefix"] = f" ▲ {index_Offset}" #If the song went up
                        elif old_Index == index_New:
                            NEW_TopData["items"][index_New]["prefix"] = "" #If no changes happened

    return NEW_TopData



def get_User_Top_Artists(user_Unique_ID, entities_Limit=50, offset=0, time_Range="short_term"):
    """
    Get a list of the user's top performers

    user_Unique_ID - Internal unique user ID

    entities_Limit - Selection limit

    offset - Offset of the sample

    time_Range - Time range to sample (short_term, medium_term, long_term)
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    user_Top = spotify_Api.get_User_Tops(user_Auth_Token, "artists", entities_Limit, offset, time_Range)

    if not user_Top["total"] >= 1: #Checking for the presence of at least one element
        raise spotify_Exceptions.no_Tops_Data

    creation_Timestamp = int(time.time())

    NEW_TopData = {
        "entities_Limit":entities_Limit,
        "offset":offset,
        "time_Range":time_Range,
        "creation_Timestamp":creation_Timestamp,
        "comparsion_Timestamp":None,
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
    
    database_User_Artists = database_Manager.search_In_Database(user_Unique_ID, "users_TopArtists", "user_Unique_ID") #For comparison, we load the old cache of the user's top

    if database_User_Artists:
        if time_Range == "short_term":
            user_Artists = database_User_Artists[0][1]
        elif time_Range == "medium_term":
            user_Artists = database_User_Artists[0][2]
        elif time_Range == "long_term":
            user_Artists = database_User_Artists[0][3]
        
        if user_Artists: #Check if there is an old artists cache
            OLD_TopData = json.loads(user_Artists) #Deserialize the string into a dictionary

            if OLD_TopData["time_Range"] == time_Range: #If the sample time period is the same, then we make a comparison
                NEW_TopData["comparsion_Timestamp"] = OLD_TopData["creation_Timestamp"] 

                OLD_URIS = [] #Changes are tracked by ID, so we make a list of the old selection
                for index in range(len(OLD_TopData["items"])):
                    OLD_URIS.append(OLD_TopData["items"][index]["URI"])

                NEW_URIS = [] #New selection list
                for index in range(len(NEW_TopData["items"])):
                    NEW_URIS.append(NEW_TopData["items"][index]["URI"])
        
                for index_New in range(len(NEW_URIS)): #Comparing the sample for the new sample
                    try:
                        old_Index = OLD_URIS.index(NEW_URIS[index_New])
                    except:
                        NEW_TopData["items"][index_New]["prefix"] = "● " #If there is no such artist in the old sample, we put the label of the new artist
                    else:
                        if old_Index < index_New:
                            index_Offset = str(index_New - old_Index)
                            NEW_TopData["items"][index_New]["prefix"] = f" ▼ +{index_Offset}" #If the artist went up
                        elif old_Index > index_New:
                            index_Offset = str(index_New - old_Index)
                            NEW_TopData["items"][index_New]["prefix"] = f" ▲ {index_Offset}" #If the artist went down
                        elif old_Index == index_New:
                            NEW_TopData["items"][index_New]["prefix"] = "" #If no changes happened

    return NEW_TopData



def create_Top_Tracks_Playlist(user_Unique_ID, localization_Data, time_Range):
    """
    Create a playlist with the user's top songs

    user_Unique_ID - Internal unique user ID
    """
    check_Token_Lifetime(user_Unique_ID)
    database_User_Data = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")
    user_Auth_Token = database_User_Data[0][4]
    user_Spotify_ID = database_User_Data[0][1]

    database_User_Tracks = database_Manager.search_In_Database(user_Unique_ID, "users_TopTracks", "user_Unique_ID")

    if database_User_Tracks:
        if time_Range == "short_term":
            user_Tracks = database_User_Tracks[0][1]
        elif time_Range == "medium_term":
            user_Tracks = database_User_Tracks[0][2]
        elif time_Range == "long_term":
            user_Tracks = database_User_Tracks[0][3]

    top_Data = json.loads(user_Tracks)

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
    Create a music quiz from top tracks

    user_Unique_ID - Internal unique user ID

    Returns the musicQuiz_Error_NoTracks exception in case of an error (there are not enough tracks for the quiz)

    time_Range - Time range to sample (short_term, medium_term, long_term)
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    user_Top = spotify_Api.get_User_Tops(user_Auth_Token, "tracks", 50, 0, time_Range)

    if not user_Top["total"] >= 50: #Checking for a complete top
        raise spotify_Exceptions.no_Tops_Data

    top_Tracks = []
    for item in range(50): #Bring all elements to human form
        if user_Top["items"][item]["preview_url"]: #Add only preview songs to the list
            top_Tracks.append({
                "name":user_Top["items"][item]["name"],
                "artists":user_Top["items"][item]["album"]["artists"][0]["name"],
                "preview_URL":user_Top["items"][item]["preview_url"],
            })
    
    random.shuffle(top_Tracks) #Shuffle the elements of the top

    right_Answers = []
    for item in range(10): #Choose from the elements of the top 10 songs to play
        right_Answers.append({
            "name":top_Tracks[item]["name"],
            "artists":top_Tracks[item]["artists"],
            "audio_URL":top_Tracks[item]["preview_URL"],
        })

        top_Tracks.pop(item) #Remove them from the top selection

    musicQuiz_Items = {}
    musicQuiz_Items["right_Answers"] = right_Answers
    musicQuiz_Items["other_Answers"] = top_Tracks

    if len(musicQuiz_Items["right_Answers"]) < 10 or len(musicQuiz_Items["other_Answers"]) < 20:
        raise spotify_Exceptions.musicQuiz_Error_NoTracks

    return musicQuiz_Items



def get_Saved_Raw_Tracks(user_Unique_ID):
    """
    Get all user tracks as a list

    user_Unique_ID - Internal unique user ID
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]

    user_Country = spotify_Api.get_User_Profile(user_Auth_Token)["country"]
    user_Data = spotify_Api.get_Saved_Tracks(user_Auth_Token, market=user_Country)

    if user_Data["total"] == 0:
        raise spotify_Exceptions.no_Tracks

    total_Iterations = math.ceil(user_Data["total"] / 50) #Divide the number of songs for requests by 50 songs

    offset = 0
    liked_Tracks = []
    for user_Tracks in range(total_Iterations): #Get all user tracks
        user_Tracks = spotify_Api.get_Saved_Tracks(user_Auth_Token, market=user_Country, limit=50, offset=offset)

        offset += 50

        for track in range(len(user_Tracks["items"])):
            liked_Tracks.append(user_Tracks["items"][track])
        
    return liked_Tracks



def create_MusicQuiz_Liked_Songs(user_Unique_ID):
    """
    Create a Music Quiz from Liked Songs

    user_Unique_ID - Internal unique user ID

    Returns the musicQuiz_Error_NoTracks exception in case of an error (there are not enough tracks for the quiz)
    """
    liked_Tracks_Data = get_Saved_Raw_Tracks(user_Unique_ID)

    liked_Tracks = []
    for track in range(len(liked_Tracks_Data)):
        if liked_Tracks_Data[track]["track"]["preview_url"]:
            liked_Tracks.append({
                "name":liked_Tracks_Data[track]["track"]["name"],
                "artists":liked_Tracks_Data[track]["track"]["artists"][0]["name"],
                "uri":liked_Tracks_Data[track]["track"]["uri"],
                "preview_URL":liked_Tracks_Data[track]["track"]["preview_url"]
            })

    random.shuffle(liked_Tracks)

    right_Answers = []
    for item in range(10): #Select 10 tracks for right answers
        right_Answers.append({
            "name":liked_Tracks[item]["name"],
            "artists":liked_Tracks[item]["artists"],
            "audio_URL":liked_Tracks[item]["preview_URL"],
        })

        liked_Tracks.pop(item) #Remove them from the top selection

    musicQuiz_Items = {}
    musicQuiz_Items["right_Answers"] = right_Answers
    musicQuiz_Items["other_Answers"] = liked_Tracks

    if len(musicQuiz_Items["right_Answers"]) < 10 or len(musicQuiz_Items["other_Answers"]) < 20:
        raise spotify_Exceptions.musicQuiz_Error_NoTracks

    return musicQuiz_Items



def get_Several_Artists(user_Unique_ID, artists_IDs):
    """
    Get information about multiple artists

    user_Unique_ID - Internal unique user ID

    artists_IDs - LIST of Spotify Unique Artist IDs
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]

    artists_Data = spotify_Api.get_Several_Artists_Info(user_Auth_Token, artists_IDs)

    return artists_Data



def get_User_Playlists(user_Unique_ID):
    """
    Get all playlists available to the user
    """
    check_Token_Lifetime(user_Unique_ID)
    database_User_Data = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")
    user_Auth_Token = database_User_Data[0][4]
    user_Spotify_ID = database_User_Data[0][1]

    user_Playlists = spotify_Api.get_User_Playlists(user_Auth_Token)

    user_Playlists_Data = []
    for item in range(len(user_Playlists["items"])):
        playlist_Item = user_Playlists["items"][item]
        if playlist_Item["owner"]["id"] == user_Spotify_ID:
            user_Playlists_Data.append({
                "playlist_Name":playlist_Item["name"],
                "playlist_Uri":playlist_Item["uri"]
            })
    
    if len(user_Playlists_Data) == 0:
        raise spotify_Exceptions.no_Playlists
    
    return user_Playlists_Data



def get_Playlist_Tracks(user_Unique_ID, playlist_Uri):
    """
    Get all tracks from the playlist as a list
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]
    user_Country = spotify_Api.get_User_Profile(user_Auth_Token)["country"]

    playlist_Data = spotify_Api.get_Playlist_Tracks(user_Auth_Token, playlist_Uri=playlist_Uri, entities_Limit=1, market=user_Country)

    total_Iterations = math.ceil(playlist_Data["total"] / 100) #Divide the number of songs for requests by 100 songs
    offset = 0
    playlist_Tracks = []
    for _ in range(total_Iterations):
        playlist_Data = spotify_Api.get_Playlist_Tracks(user_Auth_Token, playlist_Uri=playlist_Uri, market=user_Country, entities_Limit=100, offset=offset)

        offset += 100

        for track in range(len(playlist_Data["items"])):
            playlist_Tracks.append({
                    "name":playlist_Data["items"][track]["track"]["name"],
                    "artists":playlist_Data["items"][track]["track"]["artists"][0]["name"],
                    "uri":playlist_Data["items"][track]["track"]["uri"]
                })
    
    return playlist_Tracks



def delete_Playlist_Tracks(user_Unique_ID, playlist_Uri, tracks_To_Delete):
    """
    Removes tracks from the playlist
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]

    total_Iterations = math.ceil(len(tracks_To_Delete) / 100) #Divide the number of songs for requests by 100 songs

    job_Successful = True
    for _ in range(total_Iterations):
        response = spotify_Api.delete_Playlist_Tracks(user_Auth_Token, playlist_ID=playlist_Uri, playlist_Tracks=tracks_To_Delete)

        if response == 200:
            pass
        else:
            job_Successful = False
    
    return job_Successful



def delete_Liked_Tracks(user_Unique_ID, tracks_To_Delete):
    """
    Removes tracks from Favorite Tracks section
    """
    check_Token_Lifetime(user_Unique_ID)
    user_Auth_Token = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")[0][4]

    tracks_IDs = []
    for track in range(len(tracks_To_Delete)):
        track_Item = tracks_To_Delete[track].split(":")
        print(track_Item)
        print(track_Item[-1])

        tracks_IDs.append(track_Item[-1]) #The song ID is at the end

    total_Iterations = math.ceil(len(tracks_To_Delete) / 50) #Divide the number of songs for requests by 50 songs

    job_Successful = True
    for _ in range(total_Iterations):
        response = spotify_Api.delete_Liked_Tracks(user_Auth_Token, tracks_ID=tracks_IDs)

        if response == 200:
            pass
        else:
            job_Successful = False
    
    return job_Successful



def super_Shuffle(user_Unique_ID, localization_Data, tracks_Count=None):
    """
    Create Super Shuffle from Liked Songs

    user_Unique_ID - Internal unique user ID

    tracks_Count - Number of tracks for super-shuffle (at least 100)
    """
    check_Token_Lifetime(user_Unique_ID)
    database_User_Data = database_Manager.search_In_Database(user_Unique_ID, "spotify_Users", "user_Unique_ID")
    user_Auth_Token = database_User_Data[0][4]
    user_Spotify_ID = database_User_Data[0][1]

    liked_Tracks_Data = get_Saved_Raw_Tracks(user_Unique_ID)

    liked_Tracks = []
    for track in range(len(liked_Tracks_Data)): #Pull only their uri from the list of songs
        liked_Tracks.append(liked_Tracks_Data[track]["track"]["uri"])

    for _ in range(100): #Shuffle all songs 100 times
        random.shuffle(liked_Tracks)

    playlist_Name = localization_Data["playlist_Name"]
    playlist_Name = time.strftime(playlist_Name)
    playlist_Description = localization_Data["playlist_Description"]
    new_Playlist_ID = spotify_Api.create_Playlist(user_Auth_Token, user_Spotify_ID, playlist_Name, playlist_Description)["id"] #Create a playlist and get its ID

    offset = 100
    if tracks_Count: #If the number of tracks is specified, then we cut out the number of tracks, if not, the entire sample
        total_Iterations = math.ceil(tracks_Count / offset)
    else:
        total_Iterations = math.ceil(len(liked_Tracks) / offset)

    for _ in range(total_Iterations): #We put all the songs in the playlist
        playlist_Tracks = liked_Tracks[offset - 100:offset]
        spotify_Api.add_Tracks_To_Playlist(user_Auth_Token, new_Playlist_ID, playlist_Tracks)
        offset += 100

    return new_Playlist_ID