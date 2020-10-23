import telebot
import logging
import time
import json
import urllib
from spotify_Module import localization

with open("bot_Keys.json") as bot_Keys_File:
    bot_Keys = json.load(bot_Keys_File)

spotify_Bot = telebot.TeleBot(bot_Keys["telegram"]["telegram_Key"])

language_Vocabluary = localization.load_Vocabluary()



def spotify_Login_Offer(chat_id, spotify_Auth_Link, language_Name):
    """
    Просьба о входе в аккаунт Spotify
    """
    login_Keyboard = telebot.types.InlineKeyboardMarkup()
    login_Button = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["service_Buttons"]["authorize_Spotify"], url=spotify_Auth_Link)
    login_Keyboard.add(login_Button)
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["authorization"]["spotify_Login_Offer"], parse_mode="Markdown", reply_markup=login_Keyboard)



def language_Selector(chat_id, language_Name):
    """
    Клавиатура выбора языка
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.row("English")
    keyboard.row("Russian")

    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["authorization"]["choose_Language"], parse_mode="Markdown", reply_markup=keyboard)



def language_Changed(chat_id, language_Name):
    """
    Успешная авторизация
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["language_Changed"], parse_mode="Markdown")



def user_Leaving(chat_id, language_Name):
    """
    Уведомление пользователю об успешном выходе из бота
    """
    disable_Keyboard = telebot.types.InlineKeyboardMarkup()
    disable_Button = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["service_Buttons"]["disable_Jarvis"], url="https://www.spotify.com/account/apps/")
    disable_Keyboard.add(disable_Button)
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["authorization"]["user_Leaving"], parse_mode="Markdown", reply_markup=disable_Keyboard)



def auth_Complete(chat_id, user_Nickname, language_Name):
    """
    Успешная авторизация
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["authorization"]["auth_Complete"].format(user_Nickname=user_Nickname), parse_mode="Markdown")



def send_Developer_Contacts(chat_id, language_Name):
    """
    Отправить контакты разработчика
    """
    links_Keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    discord_Button = telebot.types.InlineKeyboardButton(text="Discord", url="https://discord.gg/Z4A4qdw")
    vk_Button = telebot.types.InlineKeyboardButton(text="VK", url="https://vk.com/koteyk0o")
    links_Keyboard.add(discord_Button, vk_Button)
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["authorization"]["developer_Contacts"], parse_mode="Markdown", reply_markup=links_Keyboard)    



def superShuffle_Description(chat_id, language_Name):
    """
    Описание функции супер-шаффл
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["superShuffle"]["superShuffle_Description"], parse_mode="Markdown")



def yourTops_Description(chat_id, language_Name):
    """
    Описание функции ваши-топы
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["yourTops"]["yourTops_Description"], parse_mode="Markdown")



def controls_Main_Menu(chat_id, language_Name):
    """
    Клавиатура основного меню
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["now_Playing"])
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["youtube_Clip"], language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["super_Shuffle"])
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["your_Tops"], language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["musicQuiz"])
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["choose_Category"], reply_markup=keyboard)



def send_MusicQuiz_Round(chat_id, musicQuiz_Round_Data, language_Name):
    """
    Отправить пользователю музыкальную викторину
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    keyboard.row(musicQuiz_Round_Data["keyboard"][0])
    keyboard.row(musicQuiz_Round_Data["keyboard"][1])
    keyboard.row(musicQuiz_Round_Data["keyboard"][2])
    keyboard.row(musicQuiz_Round_Data["keyboard"][3])

    musicQuiz_Round = musicQuiz_Round_Data["current_Round"] + 1
    audio_Title = f"Round #{musicQuiz_Round}"
    audio_File = urllib.request.urlopen(musicQuiz_Round_Data["audio_URL"]).read()

    spotify_Bot.send_audio(chat_id, audio=audio_File, title=audio_Title, caption=language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["musicQuiz_Question"], reply_markup=keyboard)



def musicQuiz_Rules(chat_id, language_Name):
    """
    Отправить пользователю правила игры в музыкальную викторину
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["musicQuiz_Rules"], parse_mode="Markdown")



def shuffle_Tracks_Count(chat_id, language_Name):
    """
    Вопрос пользователю о количестве треков для супер-шаффла
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["offset_Size"]["100_Songs"], language_Vocabluary[language_Name]["keyboard_Buttons"]["offset_Size"]["200_Songs"], language_Vocabluary[language_Name]["keyboard_Buttons"]["offset_Size"]["all_Offset"], language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"])
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["superShuffle"]["tracks_Count_Question"], reply_markup=keyboard)



def tops_Type_Select(chat_id, language_Name):
    """
    Вопрос пользователю о типе топа
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["songs"], language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["artists"], language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"])
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["yourTops"]["select_Top_Type"], reply_markup=keyboard)



def tops_Time_Period(chat_id, language_Name):
    """
    Вопрос пользователю о периоде выборки для топа
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["time_Buttons"]["4_Weeks"], language_Vocabluary[language_Name]["keyboard_Buttons"]["time_Buttons"]["6_Months"], language_Vocabluary[language_Name]["keyboard_Buttons"]["time_Buttons"]["all_Time"])
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["yourTops"]["select_Top_Time"], reply_markup=keyboard)



def musicQuiz_Type_Select(chat_id, language_Name):
    """
    Вопрос пользователю о выборке для викторины
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["liked_Songs"], language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["top_Songs"], language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"])
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["quiz_Section"], reply_markup=keyboard)



def tracks_Top(chat_id, top_Data, language_Name):
    """
    Вывод топа песен пользователя
    """
    keyboard = telebot.types.InlineKeyboardMarkup()
    create_Playlist_Button = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["create_Playlist"], callback_data="interface???playlist???create???topTracksPlaylist")
    keyboard.add(create_Playlist_Button)

    chat_Top_Data = {}
    chat_Top_Data["top_Summary"] = language_Vocabluary[language_Name]["chat_Messages"]["yourTops"]["top_Songs_Header"] + "\n\n"

    for top_Item in range(10):
        artists = top_Data["items"][top_Item]["artists"]
        name = top_Data["items"][top_Item]["name"]
        chat_Top_Data[top_Item] = f"<b>{top_Item + 1}.</b> {artists} - {name} \n\n"
        chat_Top_Data["top_Summary"] += chat_Top_Data[top_Item]

    spotify_Bot.send_message(chat_id, chat_Top_Data["top_Summary"], reply_markup=keyboard, parse_mode="HTML")



def artists_Top(chat_id, top_Data, language_Name):
    """
    Вывод топа исполнителей пользователя
    """
    chat_Top_Data = {}
    chat_Top_Data["top_Summary"] = language_Vocabluary[language_Name]["chat_Messages"]["yourTops"]["top_Artists_Header"] + "\n\n"

    for top_Item in range(10):
        name = top_Data["items"][top_Item]["name"]
        followers = top_Data["items"][top_Item]["followers"]
        chat_Top_Data[top_Item] = f"<b>{top_Item + 1}.</b> {name} - {followers} Followers \n\n"
        chat_Top_Data["top_Summary"] += chat_Top_Data[top_Item]

    spotify_Bot.send_message(chat_id, chat_Top_Data["top_Summary"], parse_mode="HTML")



def astray_Notification(chat_id, language_Name):
    """
    Сообщить пользователю о возможности вызова клавиатуры
    """ 
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["astray_Notification"], parse_mode="Markdown")



def insufficient_Data_For_Top(chat_id, language_Name):
    """
    Не хватает песен для составления топа
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["yourTops"]["insufficient_Data_For_Top"], parse_mode="Markdown")



def no_ActiveDevices(chat_id, language_Name):
    """
    Нет активных устройств для начала воспроизведения
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["errors"]["start_Playing_NoDevice"], parse_mode="Markdown")



def premium_Required(chat_id, language_Name):
    """
    Для начала воспроизведения требуется премиум-подписка
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["errors"]["start_Playing_PremiumRequired"], parse_mode="Markdown")



def playback_Error(chat_id, language_Name):
    """
    Невозможно начать воспроизведение
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["errors"]["start_Playing_RequestError"], parse_mode="Markdown")



def playback_Started(chat_id, language_Name):
    """
    Воспроизведение началось
    """
    playback_Text = language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["playback_Started"]
    spotify_Bot.send_message(chat_id, playback_Text, parse_mode="Markdown")



def now_Playing_Error(chat_id, language_Name):
    """
    Недостаточно метаданных для отображения
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["errors"]["now_Playing_Error"], parse_mode="Markdown")



def search_Clip(chat_id, language_Name):
    """
    Клип в процессе поиска
    """
    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["youTube"]["searching_Clip"], reply_markup=markup, parse_mode="Markdown")



def musicQuiz_Preparing(chat_id, language_Name):
    """
    Игровая сессия подготавливается
    """
    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["musicQuiz_Preparing"], reply_markup=markup, parse_mode="Markdown")



def musicQuiz_Incorrect_Answer(chat_id, musicQuiz_Round_Stats, language_Name):
    """
    Неправильный ответ викторины
    """

    right_Answer = musicQuiz_Round_Stats["round_Answer"]
    took_Time_Answer = int(time.time()) - musicQuiz_Round_Stats["round_Prepared_Timestamp"]
    message_Text = language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["musicQuiz_Incorrect_Answer"].format(right_Answer=right_Answer, took_Time_Answer=took_Time_Answer)

    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    spotify_Bot.send_message(chat_id, message_Text, reply_markup=markup, parse_mode="HTML")



def musicQuiz_Correct_Answer(chat_id, musicQuiz_Round_Stats, language_Name):
    """
    Правильный ответ викторины
    """

    right_Answer = musicQuiz_Round_Stats["round_Answer"]
    took_Time_Answer = int(time.time()) - musicQuiz_Round_Stats["round_Prepared_Timestamp"]
    message_Text = language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["musicQuiz_Correct_Answer"].format(right_Answer=right_Answer, took_Time_Answer=took_Time_Answer)

    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    spotify_Bot.send_message(chat_id, message_Text, reply_markup=markup, parse_mode="HTML")



def musicQuiz_Answer_Timeout(chat_id, musicQuiz_Round_Stats, language_Name):
    """
    Закончилось время на ответ викторины
    """

    right_Answer = musicQuiz_Round_Stats["round_Answer"]
    took_Time_Answer = int(time.time()) - musicQuiz_Round_Stats["round_Prepared_Timestamp"]
    message_Text = language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["musicQuiz_Answer_Timeout"].format(right_Answer=right_Answer, took_Time_Answer=took_Time_Answer)

    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    spotify_Bot.send_message(chat_id, message_Text, reply_markup=markup, parse_mode="HTML")



def musicQuiz_End(chat_id, musicQuiz_Statistic, language_Name):
    """
    Конец музыкальной викторины
    """
    markup = telebot.types.ReplyKeyboardRemove(selective=False)

    total_Rounds = musicQuiz_Statistic["total_Rounds"]
    correct_Answers = musicQuiz_Statistic["correct_Answers"]
    message_Text = language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["musicQuiz_End"].format(total_Rounds=total_Rounds, correct_Answers=correct_Answers)
    spotify_Bot.send_message(chat_id, message_Text, reply_markup=markup, parse_mode="Markdown")



def musicQuiz_Error_NoTracks(chat_id, language_Name):
    """
    Ошибка MusicQuiz - не хватило треков для начала игры
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["musicQuiz_Error_NoSongs"], parse_mode="Markdown")



def musicQuiz_Error_RoundProcess(chat_id, language_Name):
    """
    Ошибка MusicQuiz - возникла ошибка при обработке раунда
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["musicQuiz_Error_RoundProcess"], parse_mode="Markdown")



def insufficient_Data_For_MusicQuiz(chat_id, language_Name):
    """
    Недостаточно песен для музыкальной викторины
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["insufficient_Data_For_MusicQuiz"], parse_mode="Markdown")



def insufficient_Data_For_Shuffle(chat_id, language_Name):
    """
    Недостаточно песен для супер-шаффла
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["superShuffle"]["insufficient_Data_For_Shuffle"], parse_mode="Markdown")



def nowplaying_Nothing(chat_id, language_Name):
    """
    В данный момент ничего не играет
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["nowplaying_Nothing"], parse_mode="Markdown")



def cannot_Authorize(chat_id, language_Name):
    """
    Ошибка авторизации пользователя
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["errors"]["cannot_Authorize"], parse_mode="Markdown")



def servers_Link_Error(chat_id, language_Name):
    """
    Ошибка связи с серверами Спотифая
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["errors"]["servers_Link_Error"], parse_mode="Markdown")



def unknown_Error(chat_id, language_Name):
    """
    Неизвестная ошибка
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["errors"]["unknown_Error"], parse_mode="Markdown")



def denied_Work_Reason(chat_id, language_Name):
    """
    Пока выполняется работа, вы не можете использовать эту функцию
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["errors"]["denied_Work_Reason"], parse_mode="Markdown")



def playlist_Preparing(chat_id, language_Name, hide_Keyboard=True):
    """
    Плейлист готовится
    """
    if hide_Keyboard:
        markup = telebot.types.ReplyKeyboardRemove(selective=False)
        spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["playlist_Preparing"], reply_markup=markup, parse_mode="Markdown")

    else:
        spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["playlist_Preparing"], parse_mode="Markdown")        



def function_On_Way(chat_id, language_Name):
    """
    Функция скоро появится
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["function_On_Way"], parse_mode="Markdown")



def jarvis_Updated(chat_id, language_Name):
    """
    Джарвис был обновлен
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["jarvis_Updated"], parse_mode="Markdown")



def playlist_Ready(chat_id, playlist_Data, language_Name):
    """
    Плейлист готов
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    play_Playlist_Data = "player???play???" + playlist_Data["playlist_ID"] #Шифровка callback даты для последующего парсинга (ограничение в 64 байта)

    play_Playlist = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["play_On_Spotify"], callback_data=play_Playlist_Data)
    open_Playlist = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["open_On_Spotify"], url=playlist_Data["external_URL"])
    keyboard.add(play_Playlist)
    keyboard.add(open_Playlist)

    ready_Data = {}
    ready_Data["name"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["playlist_Name"] + playlist_Data["name"] + "\n"
    ready_Data["description"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["playlist_Description"] + playlist_Data["description"] + "\n"
    ready_Data["total_Tracks"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["playlist_Total_Tracks"] + str(playlist_Data["total_Tracks"]) + "\n"
    ready_Data["playlist_Summary"] = ready_Data["name"] + ready_Data["description"] + ready_Data["total_Tracks"]

    ready_Text = language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["playlist_Ready"] + "\n\n" + ready_Data["playlist_Summary"]
    playlist_Cover = urllib.request.urlopen(playlist_Data["image_URL"]).read()

    spotify_Bot.send_photo(chat_id, playlist_Cover, caption=ready_Text, reply_markup=keyboard, parse_mode="HTML")



def now_Playing(chat_id, playing_Data, language_Name):
    """
    Вывод сейчас играет
    """
    now_Playing_Data = {}
    now_Playing_Data["artists"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["player_Artist"] + ", ".join(playing_Data["artists"]) + "\n"
    now_Playing_Data["album_Name"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["player_Album"] + playing_Data["album_Name"] + "\n"
    now_Playing_Data["song_Name"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["player_Song"] + playing_Data["song_Name"] + "\n"
    now_Playing_Data["song_Duration"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["player_Duration"] + time.strftime("%M:%S", time.gmtime(playing_Data["song_Duration"] / 1000)) + "\n"
    now_Playing_Data["playback_Summary"] = now_Playing_Data["song_Name"] + now_Playing_Data["artists"] + now_Playing_Data["album_Name"] + now_Playing_Data["song_Duration"]

    playback_Text = language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["now_Playing"] + "\n\n" + now_Playing_Data["playback_Summary"]
    playback_Cover = urllib.request.urlopen(playing_Data["song_Cover_URL"]).read()

    spotify_Bot.send_photo(chat_id, playback_Cover, caption=playback_Text, parse_mode="HTML")



def clip_Message(chat_id, playing_Data, language_Name):
    """
    Вывод клипа
    """
    now_Playing_Data = {}
    now_Playing_Data["artists"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["player_Artist"] + ", ".join(playing_Data["artists"]) + "\n"
    now_Playing_Data["song_Name"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["player_Song"] + playing_Data["song_Name"] + "\n\n"
    now_Playing_Data["youtube_Clip_Link"] = playing_Data["youtube_URL"]
    now_Playing_Data["playback_Summary"] = now_Playing_Data["artists"] + now_Playing_Data["song_Name"] + now_Playing_Data["youtube_Clip_Link"]

    playback_Text = language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["now_Playing"] + "\n\n" + now_Playing_Data["playback_Summary"]

    spotify_Bot.send_message(chat_id, text=playback_Text, parse_mode="HTML")
