import telebot
import time
import json
from datetime import datetime
from spotify_Module import localization

with open("bot_Keys.json") as bot_Keys_File:
    bot_Keys = json.load(bot_Keys_File)

spotify_Bot = telebot.TeleBot(bot_Keys["telegram"]["telegram_Key"])

language_Vocabluary = localization.load_Vocabluary()



def share_Inline_NowPlaying(inline_ID, playing_Data, language_Name):
    """
    Вывод сейчас играет
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    song_ID = playing_Data["song_ID"]
    play_On_Spotify = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["play_On_Spotify"], callback_data=f"player#play#track#{song_ID}")
    keyboard.add(play_On_Spotify)

    if playing_Data["youtube_URL"]: #Если клип песни есть, создаем кнопку
        youtube_Button = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["youtube_Clip"], url=playing_Data["youtube_URL"])
        keyboard.add(youtube_Button)

    song_Link = playing_Data["external_URL"]
    song_Name = playing_Data["song_Name"]
    html_Link = f'<a href="{song_Link}">{song_Name}</a>'

    nowPlaying_Info = {}
    nowPlaying_Info["song_Name"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["song"] + html_Link + "\n"
    nowPlaying_Info["artists"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["artist"] + ", ".join(playing_Data["artists"]) + "\n"
    nowPlaying_Info["album_Name"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["album"] + playing_Data["album_Name"] + "\n"
    nowPlaying_Info["release_date"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["release_date"] + playing_Data["release_Date"] + "\n"    
    nowPlaying_Info["song_Duration"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["duration"] + time.strftime("%M:%S", time.gmtime(playing_Data["song_Duration"] / 1000))
    
    if playing_Data["preview_URL"]: #Если превью нет, уведомляем об этом
        nowPlaying_Info["preview_URL"] = ""
    else:
        nowPlaying_Info["preview_URL"] = "\n\n" + language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["preview_Not_Available"]

    if len(playing_Data["images"]) > 0: #Если существует обложка альбома
        if len(playing_Data["images"]) > 1: #Если больше 1, то значит их там 3! (наверное)
            nowPlaying_Info["full_Image"] = playing_Data["images"][1]
            nowPlaying_Info["preview_Image"] = playing_Data["images"][2]
            nowPlaying_Info["article_Cover"] = playing_Data["images"][2]["url"]
        else:
            nowPlaying_Info["full_Image"] = playing_Data["images"][0]
            nowPlaying_Info["preview_Image"] = playing_Data["images"][0]
            nowPlaying_Info["article_Cover"] = playing_Data["images"][0]["url"]
    else:
        nowPlaying_Info["full_Image"] = None
        nowPlaying_Info["preview_Image"] = None
        nowPlaying_Info["article_Cover"] = None

    nowPlaying_Info["playback_Summary"] = nowPlaying_Info["song_Name"] + nowPlaying_Info["artists"] + nowPlaying_Info["album_Name"] + nowPlaying_Info["release_date"] + nowPlaying_Info["song_Duration"] + nowPlaying_Info["preview_URL"]
    playback_Text = language_Vocabluary[language_Name]["chat_Messages"]["sharing_Headers"]["song_Listening_Now"] + "\n\n" + nowPlaying_Info["playback_Summary"]

    if playing_Data["preview_URL"]:
        results = telebot.types.InlineQueryResultAudio(1,
        playing_Data["preview_URL"],
        title=playing_Data["song_Name"],
        performer=playing_Data["artists"][0],
        caption=playback_Text,
        parse_mode="HTML",
        reply_markup=keyboard)
    else:
        results = telebot.types.InlineQueryResultArticle(1,
        title=playing_Data["song_Name"],
        input_message_content=telebot.types.InputTextMessageContent(playback_Text, parse_mode="HTML"),
        reply_markup=keyboard,
        description=playing_Data["artists"][0],
        thumb_url=nowPlaying_Info["article_Cover"])
    
    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=[results], cache_time=0)



def share_Inline_Album(inline_ID, album_Data, language_Name):
    """
    Вывод альбома
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    album_ID = album_Data["id"]
    play_On_Spotify = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["play_On_Spotify"], callback_data=f"player#play#album#{album_ID}")
    keyboard.add(play_On_Spotify)

    album_Link = album_Data["external_URL"]
    album_Name = album_Data["name"]
    html_Link = f'<a href="{album_Link}">{album_Name}</a>'
    
    album_Info = {}
    album_Info["name"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["name"] + html_Link + "\n"
    album_Info["artists"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["artist"] + ", ".join(album_Data["artists"]) + "\n"
    album_Info["label"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["label"] + album_Data["label"] + "\n"
    album_Info["release_Date"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["release_date"] + album_Data["release_Date"] + "\n"
    album_Info["total_Tracks"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["total_Tracks"] + str(album_Data["total_Tracks"]) + "\n"

    if len(album_Data["images"]) > 0: #Если существует обложка альбома
        if len(album_Data["images"]) > 1: #Если больше 1, то значит их там 3! (наверное)
            album_Info["full_Image"] = album_Data["images"][1]
            album_Info["preview_Image"] = album_Data["images"][2]
            album_Info["article_Cover"] = album_Data["images"][2]["url"]
        else:
            album_Info["full_Image"] = album_Data["images"][0]
            album_Info["preview_Image"] = album_Data["images"][0]
            album_Info["article_Cover"] = album_Data["images"][0]["url"]
    else:
        album_Info["full_Image"] = None
        album_Info["preview_Image"] = None
        album_Info["article_Cover"] = None
    
    album_Info["info_Summary"] = album_Info["name"] + album_Info["artists"] + album_Info["label"] + album_Info["release_Date"] + album_Info["total_Tracks"]

    album_Info_Summary = language_Vocabluary[language_Name]["chat_Messages"]["sharing_Headers"]["album_Listening_Now"] + "\n\n" + album_Info["info_Summary"]

    results = telebot.types.InlineQueryResultArticle(1,
    title=language_Vocabluary[language_Name]["inline_Metadata"]["album"],
    input_message_content=telebot.types.InputTextMessageContent(album_Info_Summary, parse_mode="HTML"),
    reply_markup=keyboard,
    description=album_Data["name"],
    thumb_url=album_Info["article_Cover"])

    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=[results], cache_time=0)



def share_Inline_Artist(inline_ID, artist_Data, language_Name):
    """
    Вывод исполнителя
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    artist_ID = artist_Data["id"]
    play_On_Spotify = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["play_On_Spotify"], callback_data=f"player#play#artist#{artist_ID}")
    keyboard.add(play_On_Spotify)

    artist_Link = artist_Data["external_URL"]
    artist_Name = artist_Data["name"]
    html_Link = f'<a href="{artist_Link}">{artist_Name}</a>'

    artist_Info = {}
    artist_Info["artist"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["artist"] + html_Link + "\n"
    artist_Info["genres"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["genres"] + ", ".join(artist_Data["genres"]) + "\n"
    artist_Info["followers"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["followers"] + str(artist_Data["followers"]) + "\n"
    artist_Info["info_Summary"] = artist_Info["artist"] + artist_Info["genres"] + artist_Info["followers"]

    if len(artist_Data["images"]) > 0: #Если существует обложка альбома
        if len(artist_Data["images"]) > 1: #Если больше 1, то значит их там 3! (наверное)
            artist_Info["full_Image"] = artist_Data["images"][1]
            artist_Info["preview_Image"] = artist_Data["images"][2]
            artist_Info["article_Cover"] = artist_Data["images"][2]["url"]
        else:
            artist_Info["full_Image"] = artist_Data["images"][0]
            artist_Info["preview_Image"] = artist_Data["images"][0]
            artist_Info["article_Cover"] = artist_Data["images"][0]["url"]
    else:
        artist_Info["full_Image"] = None
        artist_Info["preview_Image"] = None
        artist_Info["article_Cover"] = None

    artist_Info_Summary = language_Vocabluary[language_Name]["chat_Messages"]["sharing_Headers"]["artist_Listening_Now"] + "\n\n" + artist_Info["info_Summary"]

    results = telebot.types.InlineQueryResultArticle(1,
    title=language_Vocabluary[language_Name]["inline_Metadata"]["artist"],
    description=artist_Data["name"],
    input_message_content=telebot.types.InputTextMessageContent(artist_Info_Summary, parse_mode="HTML"),
    reply_markup=keyboard,
    thumb_url=artist_Info["article_Cover"])

    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=[results], cache_time=0)



def share_Inline_Playlist(inline_ID, playlist_Data, language_Name):
    """
    Вывод плейлиста
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    playlist_ID = playlist_Data["playlist_ID"]
    play_On_Spotify = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["play_On_Spotify"], callback_data=f"player#play#playlist#{playlist_ID}")
    keyboard.add(play_On_Spotify)

    playlist_Link = playlist_Data["external_URL"]
    playlist_Name = playlist_Data["name"]
    html_Link = f'<a href="{playlist_Link}">{playlist_Name}</a>'

    playlist_Info = {}
    playlist_Info["name"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["name"] + html_Link + "\n"

    if playlist_Data["description"]:
        playlist_Info["description"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["description"] + playlist_Data["description"] + "\n"
    else:
        playlist_Info["description"] = ""
    
    playlist_Info["total_Tracks"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["total_Tracks"] + str(playlist_Data["total_Tracks"]) + "\n"
    playlist_Info["playlist_Summary"] = playlist_Info["name"] + playlist_Info["description"] + playlist_Info["total_Tracks"]

    if len(playlist_Data["images"]) > 0: #Если существует обложка альбома
        if len(playlist_Data["images"]) > 1: #Если больше 1, то значит их там 3! (наверное)
            playlist_Info["full_Image"] = playlist_Data["images"][1]
            playlist_Info["preview_Image"] = playlist_Data["images"][2]
            playlist_Info["article_Cover"] = playlist_Data["images"][2]["url"]
        else:
            playlist_Info["full_Image"] = playlist_Data["images"][0]
            playlist_Info["preview_Image"] = playlist_Data["images"][0]
            playlist_Info["article_Cover"] = playlist_Data["images"][0]["url"]
    else:
        playlist_Info["full_Image"] = None
        playlist_Info["preview_Image"] = None
        playlist_Info["article_Cover"] = None

    playlist_Info_Summary = language_Vocabluary[language_Name]["chat_Messages"]["sharing_Headers"]["playlist_Listening_Now"] + "\n\n" + playlist_Info["playlist_Summary"]

    results = telebot.types.InlineQueryResultArticle(1,
    title=language_Vocabluary[language_Name]["inline_Metadata"]["playlist"],
    description=playlist_Data["name"],
    input_message_content=telebot.types.InputTextMessageContent(playlist_Info_Summary, parse_mode="HTML"),
    reply_markup=keyboard,
    thumb_url=playlist_Info["article_Cover"])

    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=[results], cache_time=0)



def search_Results(inline_ID, search_Results, language_Name):
    """
    Вывод результатов поиска
    """
    answer_Results = []
    for song in range(len(search_Results["tracks"])):
        song_Item = search_Results["tracks"][song]
        keyboard = telebot.types.InlineKeyboardMarkup()

        song_ID = song_Item["song_ID"]
        play_On_Spotify = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["play_On_Spotify"], callback_data=f"player#play#track#{song_ID}")
        keyboard.add(play_On_Spotify)

        song_Link = song_Item["external_URL"]
        song_Name = song_Item["song_Name"]
        html_Link = f'<a href="{song_Link}">{song_Name}</a>'

        song_Info = {}
        song_Info["song_Name"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["song"] + html_Link + "\n"
        song_Info["artists"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["artist"] + ", ".join(song_Item["artists"]) + "\n"
        song_Info["album_Name"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["album"] + song_Item["album_Name"] + "\n"
        song_Info["release_date"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["release_date"] + song_Item["release_Date"] + "\n"    
        song_Info["song_Duration"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["duration"] + time.strftime("%M:%S", time.gmtime(song_Item["song_Duration"] / 1000))

        if len(song_Item["images"]) > 0: #Если существует обложка альбома
            if len(song_Item["images"]) > 1: #Если больше 1, то значит их там 3! (наверное)
                song_Info["full_Image"] = song_Item["images"][1]
                song_Info["preview_Image"] = song_Item["images"][2]
                song_Info["article_Cover"] = song_Item["images"][2]["url"]
            else:
                song_Info["full_Image"] = song_Item["images"][0]
                song_Info["preview_Image"] = song_Item["images"][0]
                song_Info["article_Cover"] = song_Item["images"][0]["url"]
        else:
            song_Info["full_Image"] = None
            song_Info["preview_Image"] = None
            song_Info["article_Cover"] = None
            
        song_Info["playback_Summary"] = song_Info["song_Name"] + song_Info["artists"] + song_Info["album_Name"] + song_Info["release_date"] + song_Info["song_Duration"]

        if song_Item["preview_URL"]:
            answer_Results.append(telebot.types.InlineQueryResultAudio(song,
            song_Item["preview_URL"],
            title=song_Item["song_Name"],
            performer=song_Item["artists"][0],
            caption=song_Info["playback_Summary"],
            parse_mode="HTML",
            reply_markup=keyboard))
        else:
            answer_Results.append(telebot.types.InlineQueryResultArticle(song,
            title=song_Item["song_Name"],
            input_message_content=telebot.types.InputTextMessageContent(song_Info["playback_Summary"], parse_mode="HTML"),
            reply_markup=keyboard,
            description=song_Item["artists"][0],
            thumb_url=song_Info["article_Cover"]))        
        
    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=answer_Results, cache_time=0)



def inline_NowPlaying_Error(inline_ID, language_Name):
    """
    Ошибка, песня не содержит всех метаданных
    """
    results = telebot.types.InlineQueryResultArticle(1,
    title=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["nowPlaying_NoData"]["title"],
    input_message_content=telebot.types.InputTextMessageContent(language_Vocabluary[language_Name]["inline_Messages"]["errors"]["nowPlaying_NoData"]["description"]),
    description=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["nowPlaying_NoData"]["description"])

    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=[results], cache_time=0)



def inline_NowPlaying_Nothing(inline_ID, language_Name):
    """
    Ошибка, сейчас ничего не играет
    """
    results = telebot.types.InlineQueryResultArticle(1,
    title=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["nowPlaying_Nothing"]["title"],
    input_message_content=telebot.types.InputTextMessageContent(language_Vocabluary[language_Name]["inline_Messages"]["errors"]["nowPlaying_Nothing"]["description"]),
    description=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["nowPlaying_Nothing"]["description"])

    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=[results], cache_time=0)



def inline_Unknown_Error(inline_ID, language_Name):
    """
    Ошибка, неизвестная ошибка
    """
    results = telebot.types.InlineQueryResultArticle(1,
    title=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["unknown_Error"]["title"],
    input_message_content=telebot.types.InputTextMessageContent(language_Vocabluary[language_Name]["inline_Messages"]["errors"]["unknown_Error"]["description"]),
    description=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["unknown_Error"]["description"])

    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=[results], cache_time=0)



def inline_Spotify_Not_Authorized(inline_ID, language_Name):
    """
    Ошибка, аккаунт Spotify не авторизован
    """
    results = telebot.types.InlineQueryResultArticle(1,
    title=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["spotify_Not_Authorized"]["title"],
    input_message_content=telebot.types.InputTextMessageContent(language_Vocabluary[language_Name]["inline_Messages"]["errors"]["spotify_Not_Authorized"]["description"]),
    description=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["spotify_Not_Authorized"]["description"])

    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=[results], cache_time=0)



def inline_Auth_Error(inline_ID, language_Name):
    """
    Ошибка, ошибка авторизации Spotify аккаунта
    """
    results = telebot.types.InlineQueryResultArticle(1,
    title=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["oauth_Error"]["title"],
    input_message_content=telebot.types.InputTextMessageContent(language_Vocabluary[language_Name]["inline_Messages"]["errors"]["oauth_Error"]["description"]),
    description=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["oauth_Error"]["description"])

    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=[results], cache_time=0)



def inline_No_Context(inline_ID, language_Name):
    """
    Ошибка, невозможно получить контекст воспроизведения
    """
    results = telebot.types.InlineQueryResultArticle(1,
    title=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["no_Playback_Context"]["title"],
    input_message_content=telebot.types.InputTextMessageContent(language_Vocabluary[language_Name]["inline_Messages"]["errors"]["no_Playback_Context"]["description"]),
    description=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["no_Playback_Context"]["description"])

    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=[results], cache_time=0)



def inline_Private_Session(inline_ID, language_Name):
    """
    Ошибка, активна приватная сессия
    """
    results = telebot.types.InlineQueryResultArticle(1,
    title=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["private_Session_Enabled"]["title"],
    input_message_content=telebot.types.InputTextMessageContent(language_Vocabluary[language_Name]["inline_Messages"]["errors"]["private_Session_Enabled"]["description"]),
    description=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["private_Session_Enabled"]["description"])

    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=[results], cache_time=0)



def search_No_Results(inline_ID, language_Name):
    """
    Ошибка, нет результатов поиска
    """
    results = telebot.types.InlineQueryResultArticle(1,
    title=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["no_Search_Results"]["title"],
    input_message_content=telebot.types.InputTextMessageContent(language_Vocabluary[language_Name]["inline_Messages"]["errors"]["no_Search_Results"]["description"]),
    description=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["no_Search_Results"]["description"])

    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=[results], cache_time=0)