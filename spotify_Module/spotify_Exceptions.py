#HTTP ERRORS
class http_Exception(Exception):
    pass

class http_Connection_Error(http_Exception):
    """
    Ошибка соединения с сервером
    """
    pass

class http_Error(http_Exception):
    """
    Ошибка HTTP
    """
    def __init__(self, http_Code, http_Reason):
        self.http_Code = http_Code
        self.http_Reason = http_Reason

class http_Unknown_Error(http_Exception):
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

class no_Playing_Context(spotify_Exception):
    """
    Нет контекста воспроизведения (например приватная сессия)
    """
    pass

class musicQuiz_Error_NoTracks(spotify_Exception):
    """
    Ошибка MusicQuiz - не хватает песен для игры
    """
    pass

class premium_Required(spotify_Exception):
    """
    Требуется Premium подписка
    """
    pass

class no_ActiveDevices(spotify_Exception):
    """
    Нет активных устройств
    """
    pass

class playback_Error(spotify_Exception):
    """
    Нерабочие медиа-данные для запуска воспроизведения
    """
    pass

class private_Session_Enabled(spotify_Exception):
    """
    Активирована приватная сессия
    """
    pass