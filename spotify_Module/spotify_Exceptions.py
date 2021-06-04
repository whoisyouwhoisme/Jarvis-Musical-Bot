#HTTP ERRORS
class http_Exception(Exception):
    pass

class http_Connection_Error(http_Exception):
    """
    Server connection error
    """
    pass

class http_Error(http_Exception):
    """
    HTTP error
    """
    def __init__(self, http_Code, http_Reason):
        self.http_Code = http_Code
        self.http_Reason = http_Reason

class http_Unknown_Error(http_Exception):
    """
    Unknown HTTP Error
    """
    pass



#SPOTIFY ERRORS
class spotify_Exception(Exception):
    pass

class no_Playback(spotify_Exception):
    """
    Nothing is currently playing
    """
    pass

class local_Playing(spotify_Exception):
    """
    Local files is playing
    """
    pass

class no_Tops_Data(spotify_Exception):
    """
    Not enough data to compile the top
    """
    pass

class no_Tracks(spotify_Exception):
    """
    Not enough songs for a super-shuffle
    """
    pass

class no_Data(spotify_Exception):
    """
    Song meta data missing
    """
    pass

class no_Playing_Context(spotify_Exception):
    """
    No playback context (e.g. private session)
    """
    pass

class musicQuiz_Error_NoTracks(spotify_Exception):
    """
    MusicQuiz error - not enough songs to play
    """
    pass

class premium_Required(spotify_Exception):
    """
    Premium subscription required
    """
    pass

class no_ActiveDevices(spotify_Exception):
    """
    No active devices
    """
    pass

class playback_Error(spotify_Exception):
    """
    Inoperative media to start playback
    """
    pass

class private_Session_Enabled(spotify_Exception):
    """
    Private session activated
    """
    pass

class search_No_Results(spotify_Exception):
    """
    No search results
    """
    pass

class no_Playlists(spotify_Exception):
    """
    No playlists available
    """
    pass

class playlist_Not_Found(spotify_Exception):
    """
    Playlist not found
    """
    pass