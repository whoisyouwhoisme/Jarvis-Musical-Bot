#OAUTH ERRORS
class oauth_Exception(Exception):
    pass

class oauth_Connection_Error(oauth_Exception):
    """
    Ошибка соединения с сервером
    """
    pass

class oauth_Http_Error(oauth_Exception):
    """
    Ошибка HTTP
    """
    pass

class oauth_Unknown_Error(oauth_Exception):
    """
    Неизвестная ошибка
    """
    pass

#SPOTIFY ERRORS
class spotify_Exception(Exception):
    pass

class no_Playback(spotify_Exception):
    """
    В данный момент ничего не играет
    """
    pass

class no_Tops_Data(spotify_Exception):
    """
    Не хватает данных для составления топа
    """
    pass

class no_Tracks(spotify_Exception):
    """
    Не хватает песен для супер-шаффла
    """
    pass

class no_Data(spotify_Exception):
    """
    Не хватает мета-данных песни
    """
    pass

class musicQuiz_Error_NoTracks(spotify_Exception):
    """
    Ошибка MusicQuiz - не хватает песен для игры
    """
    pass

class musicQuiz_Error_RoundProcess(spotify_Exception):
    """
    Ошибка MusicQuiz - ошибка во время обработки нового раунда
    """
    pass

#YOUTUBE ERRORS
class youtube_Exception(Exception):
    pass

class youtube_Quota_Limit(youtube_Exception):
    """
    Закончилась квота на доступы в YouTube
    """
    pass

class youtube_No_Results(youtube_Exception):
    """
    Нет результатов поиска
    """
    pass

class youtube_Invalid_Request(youtube_Exception):
    """
    Неправильный запрос
    """
    pass

class youtube_Unknown_Error(Exception):
    """
    Неизвестная ошибка
    """
    pass

#HTTP ERRORS
class http_Exception(Exception):
    pass

class http_Connection_Error(http_Exception):
    """
    Ошибка HTTP
    """
    pass