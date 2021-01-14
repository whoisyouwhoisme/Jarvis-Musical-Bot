import telebot
import time
import json
from datetime import datetime
from spotify_Module import localization

with open("bot_Keys.json") as bot_Keys_File:
    bot_Keys = json.load(bot_Keys_File)

spotify_Bot = telebot.TeleBot(bot_Keys["telegram"]["telegram_Key"])

language_Vocabluary = localization.load_Vocabluary()



def controls_Main_Menu(chat_id, language_Name):
    """
    Клавиатура основного меню
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["inline_Help"])
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["your_Tops"], language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["super_Shuffle"], language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["musicQuiz"])
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["choose_Category"], reply_markup=keyboard)



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
    Язык сменен успешно
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["language_Changed"], parse_mode="Markdown")



def user_Leaving(chat_id, language_Name):
    """
    Уведомление пользователю об успешном выходе из бота
    """
    #Первое сообщение с кнопкой /start
    start_Keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    start_Keyboard.row("/start")
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["authorization"]["user_Leaving"], parse_mode="Markdown", reply_markup=start_Keyboard)

    #Второе сообщение с кнопкой отключения бота
    keyboard = telebot.types.InlineKeyboardMarkup()
    disable_Button = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["service_Buttons"]["disable_Jarvis"], url="https://www.spotify.com/account/apps/")
    keyboard.add(disable_Button)
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["authorization"]["disable_Bot"], parse_mode="Markdown", reply_markup=keyboard)



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
    audio_File = musicQuiz_Round_Data["audio_File"]

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
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["offset_Size"]["100_Songs"], language_Vocabluary[language_Name]["keyboard_Buttons"]["offset_Size"]["200_Songs"], language_Vocabluary[language_Name]["keyboard_Buttons"]["offset_Size"]["all_Offset"])
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"])
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["superShuffle"]["tracks_Count_Question"], reply_markup=keyboard)



def tops_Type_Select(chat_id, language_Name):
    """
    Вопрос пользователю о типе топа
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["songs"], language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["artists"])
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"])
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["yourTops"]["select_Top_Type"], reply_markup=keyboard)



def tops_Time_Period(chat_id, language_Name):
    """
    Вопрос пользователю о периоде выборки для топа
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["time_Buttons"]["4_Weeks"], language_Vocabluary[language_Name]["keyboard_Buttons"]["time_Buttons"]["6_Months"], language_Vocabluary[language_Name]["keyboard_Buttons"]["time_Buttons"]["all_Time"])
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"])
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["yourTops"]["select_Top_Time"], reply_markup=keyboard)



def musicQuiz_Type_Select(chat_id, language_Name):
    """
    Вопрос пользователю о выборке для викторины
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["liked_Songs"], language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["top_Songs"])
    keyboard.row(language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["back_To_Menu"])
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["musicQuiz"]["quiz_Section"], reply_markup=keyboard)



def tracks_Top(chat_id, top_Data, language_Name, message_ID=None):
    """
    Вывод топа песен пользователя
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    time_Range = top_Data["time_Range"]

    previous_Page = top_Data["current_Page"] - 1 #Индекс предыдущей страницы
    previous_Page_Button = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["previous_Page"], callback_data=f"interface#topTracks#page#{time_Range}#{previous_Page}")

    next_Page = top_Data["current_Page"] + 1 #Индекс следующей страницы
    next_Page_Button = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["next_Page"], callback_data=f"interface#topTracks#page#{time_Range}#{next_Page}")

    create_Playlist_Button = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["create_Playlist"], callback_data=f"interface#topTracks#createPlaylist#{time_Range}")

    keyboard.add(create_Playlist_Button) #Кнопка создания плейлиста

    if not top_Data["current_Page"] <= 1 and not top_Data["current_Page"] >= top_Data["max_Pages"]: #Херня для создания красивой клавиатуры
        keyboard.add(previous_Page_Button, next_Page_Button)
    elif not top_Data["current_Page"] <= 1:
        keyboard.add(previous_Page_Button)
    elif not top_Data["current_Page"] >= top_Data["max_Pages"]:
        keyboard.add(next_Page_Button)

    time_Range = language_Vocabluary[language_Name]["chat_Messages"]["yourTops"][time_Range]
    last_Update = datetime.utcfromtimestamp(int(top_Data["last_Update"])).strftime("%m-%d-%Y %H:%M")

    chat_Top_Data = {}
    chat_Top_Data["top_Summary"] = language_Vocabluary[language_Name]["chat_Messages"]["yourTops"]["top_Songs_Header"].format(time_Range=time_Range, previous_Page=top_Data["current_Page"], next_Page=top_Data["max_Pages"]) + "\n\n"

    chat_Top_Data["top_Summary"] += language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["last_Update"] + last_Update + "\n\n"

    for top_Item in top_Data["items"]: #Подготавливаем список песен
        prefix = top_Data["items"][top_Item]["prefix"]
        artists = top_Data["items"][top_Item]["artists"]
        name = top_Data["items"][top_Item]["name"]
        chat_Top_Data[top_Item] = f"<b>{prefix}{top_Item + 1}.</b> {artists} - {name} \n\n"
        chat_Top_Data["top_Summary"] += chat_Top_Data[top_Item]

    if message_ID: #Если предоставлен ID сообщения, то редактируем сообщение, если нет, отправляем новое
        spotify_Bot.edit_message_text(chat_Top_Data["top_Summary"], chat_id=chat_id, message_id=message_ID, reply_markup=keyboard, parse_mode="HTML")
    else:
        spotify_Bot.send_message(chat_id, chat_Top_Data["top_Summary"], reply_markup=keyboard, parse_mode="HTML")



def top_Database_Error(chat_id, language_Name):
    """
    Ошибка базы данных топов
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["yourTops"]["database_Error"], parse_mode="Markdown")



def artists_Top(chat_id, top_Data, language_Name, message_ID=None):
    """
    Вывод топа исполнителей пользователя
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    time_Range = top_Data["time_Range"]

    previous_Page = top_Data["current_Page"] - 1 #Индекс предыдущей страницы
    previous_Page_Button = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["previous_Page"], callback_data=f"interface#topArtists#page#{time_Range}#{previous_Page}")

    next_Page = top_Data["current_Page"] + 1 #Индекс следующей страницы
    next_Page_Button = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["next_Page"], callback_data=f"interface#topArtists#page#{time_Range}#{next_Page}")

    if not top_Data["current_Page"] <= 1 and not top_Data["current_Page"] >= top_Data["max_Pages"]: #Херня для создания красивой клавиатуры
        keyboard.add(previous_Page_Button, next_Page_Button)
    elif not top_Data["current_Page"] <= 1:
        keyboard.add(previous_Page_Button)
    elif not top_Data["current_Page"] >= top_Data["max_Pages"]:
        keyboard.add(next_Page_Button)

    time_Range = language_Vocabluary[language_Name]["chat_Messages"]["yourTops"][time_Range]
    last_Update = datetime.utcfromtimestamp(int(top_Data["last_Update"])).strftime("%m-%d-%Y %H:%M")

    chat_Top_Data = {}
    chat_Top_Data["top_Summary"] = language_Vocabluary[language_Name]["chat_Messages"]["yourTops"]["top_Artists_Header"].format(time_Range=time_Range, previous_Page=top_Data["current_Page"], next_Page=top_Data["max_Pages"]) + "\n\n"

    chat_Top_Data["top_Summary"] += language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["last_Update"] + last_Update + "\n\n"

    for top_Item in top_Data["items"]:
        prefix = top_Data["items"][top_Item]["prefix"]
        artist = top_Data["items"][top_Item]["artist"]
        followers = top_Data["items"][top_Item]["followers"]
        chat_Top_Data[top_Item] = f"<b>{prefix}{top_Item + 1}.</b> {artist} - {followers} Followers \n\n"
        chat_Top_Data["top_Summary"] += chat_Top_Data[top_Item]

    if message_ID: #Если предоставлен ID сообщения, то редактируем сообщение, если нет, отправляем новое
        spotify_Bot.edit_message_text(chat_Top_Data["top_Summary"], chat_id=chat_id, message_id=message_ID, reply_markup=keyboard, parse_mode="HTML")
    else:
        spotify_Bot.send_message(chat_id, chat_Top_Data["top_Summary"], reply_markup=keyboard, parse_mode="HTML")



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



def song_Added_To_Queue(chat_id, language_Name):
    """
    Песня была добавлена в список воспроизведения
    """
    playback_Text = language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["added_To_Queue"]
    spotify_Bot.send_message(chat_id, playback_Text, parse_mode="Markdown")



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



def jarvis_Updated(chat_id, language_Name, jarvis_Version):
    """
    Джарвис был обновлен
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["jarvis_Updated"].format(jarvis_Version=jarvis_Version), parse_mode="Markdown")



def playlist_Ready(chat_id, playlist_Data, language_Name):
    """
    Плейлист готов
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    playlist_ID = playlist_Data["playlist_ID"] #Шифровка callback даты для последующего парсинга (ограничение в 64 байта)
    play_On_Spotify = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["play_On_Spotify"], callback_data=f"player#play#playlist#{playlist_ID}")
    open_On_Spotify = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["open_On_Spotify"], url=playlist_Data["external_URL"])
    keyboard.add(play_On_Spotify)
    keyboard.add(open_On_Spotify)

    ready_Data = {}
    ready_Data["name"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["name"] + playlist_Data["name"] + "\n"
    ready_Data["description"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["description"] + playlist_Data["description"] + "\n"
    ready_Data["total_Tracks"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["total_Tracks"] + str(playlist_Data["total_Tracks"]) + "\n"
    ready_Data["playlist_Summary"] = ready_Data["name"] + ready_Data["description"] + ready_Data["total_Tracks"]

    ready_Text = language_Vocabluary[language_Name]["chat_Messages"]["notifications"]["playlist_Ready"] + "\n\n" + ready_Data["playlist_Summary"]

    spotify_Bot.send_photo(chat_id, playlist_Data["playlist_Cover"], caption=ready_Text, reply_markup=keyboard, parse_mode="HTML")



def inline_Mode_Help(chat_id, language_Name):
    """
    Помощь по Inline режиму
    """
    spotify_Bot.send_message(chat_id, language_Vocabluary[language_Name]["chat_Messages"]["messages"]["inline_Help"], parse_mode="Markdown")



def share_Inline_NowPlaying(inline_ID, playing_Data, language_Name):
    """
    ИНЛАЙН ОТВЕТ

    Вывод сейчас играет
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    song_ID = playing_Data["song_ID"]
    play_On_Spotify = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["play_On_Spotify"], callback_data=f"player#play#track#{song_ID}")
    keyboard.add(play_On_Spotify)

    if playing_Data["youtube_URL"]: #Если клип песни есть, создаем кнопку
        youtube_Button = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["youtube_Clip"], url=playing_Data["youtube_URL"])
        keyboard.add(youtube_Button)

    nowPlaying_Info = {}
    artists_Enum = ", ".join(playing_Data["artists"])
    song_Link = playing_Data["external_URL"]
    song_Name = playing_Data["song_Name"]
    html_Link = f'<a href="{song_Link}">{song_Name}</a>'

    nowPlaying_Info["song_Name"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["song"] + html_Link + "\n"
    nowPlaying_Info["artists"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["artist"] + artists_Enum + "\n"
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
        title="Song Preview",
        caption=playback_Text,
        parse_mode="HTML",
        reply_markup=keyboard)
    else:
        results = telebot.types.InlineQueryResultArticle(1,
        title=playing_Data["song_Name"],
        input_message_content=telebot.types.InputTextMessageContent(playback_Text, parse_mode="HTML"),
        reply_markup=keyboard,
        description=artists_Enum,
        thumb_url=nowPlaying_Info["article_Cover"])
    
    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=[results], cache_time=0)



def share_Inline_Album(inline_ID, album_Data, language_Name):
    """
    ИНЛАЙН ОТВЕТ

    Вывод альбома
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    album_ID = album_Data["id"]
    play_On_Spotify = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["play_On_Spotify"], callback_data=f"player#play#album#{album_ID}")
    open_On_Spotify = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["open_On_Spotify"], url=album_Data["external_URL"])
    keyboard.add(play_On_Spotify)
    keyboard.add(open_On_Spotify)

    album_Info = {}
    artists_Enum = ", ".join(album_Data["artists"])
    album_Link = album_Data["external_URL"]
    album_Name = album_Data["name"]
    html_Link = f'<a href="{album_Link}">{album_Name}</a>'
    
    album_Info["name"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["name"] + html_Link + "\n"
    album_Info["artists"] = language_Vocabluary[language_Name]["chat_Messages"]["metadata"]["artist"] + artists_Enum + "\n"
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
    ИНЛАЙН ОТВЕТ

    Вывод исполнителя
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    artist_ID = artist_Data["id"]
    play_On_Spotify = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["play_On_Spotify"], callback_data=f"player#play#artist#{artist_ID}")
    open_On_Spotify = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["open_On_Spotify"], url=artist_Data["external_URL"])
    keyboard.add(play_On_Spotify)
    keyboard.add(open_On_Spotify)

    artist_Info = {}
    artist_Link = artist_Data["external_URL"]
    artist_Name = artist_Data["name"]
    html_Link = f'<a href="{artist_Link}">{artist_Name}</a>'

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
    ИНЛАЙН ОТВЕТ

    Вывод плейлиста
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    playlist_ID = playlist_Data["playlist_ID"]
    play_On_Spotify = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["play_On_Spotify"], callback_data=f"player#play#playlist#{playlist_ID}")
    open_On_Spotify = telebot.types.InlineKeyboardButton(text=language_Vocabluary[language_Name]["keyboard_Buttons"]["menu_Buttons"]["open_On_Spotify"], url=playlist_Data["external_URL"])
    keyboard.add(play_On_Spotify)
    keyboard.add(open_On_Spotify)

    playlist_Info = {}
    playlist_Link = playlist_Data["external_URL"]
    playlist_Name = playlist_Data["name"]
    html_Link = f'<a href="{playlist_Link}">{playlist_Name}</a>'
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



def inline_NowPlaying_Error(inline_ID, language_Name):
    """
    ИНЛАЙН ОТВЕТ

    Ошибка "Песня не содержит всех метаданных"
    """
    results = telebot.types.InlineQueryResultArticle(1,
    title=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["nowPlaying_NoData"]["title"],
    input_message_content=telebot.types.InputTextMessageContent(language_Vocabluary[language_Name]["inline_Messages"]["errors"]["nowPlaying_NoData"]["description"]),
    description=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["nowPlaying_NoData"]["description"])

    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=[results], cache_time=0)



def inline_NowPlaying_Nothing(inline_ID, language_Name):
    """
    ИНЛАЙН ОТВЕТ

    Ошибка "Сейчас ничего не играет"
    """
    results = telebot.types.InlineQueryResultArticle(1,
    title=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["nowPlaying_Nothing"]["title"],
    input_message_content=telebot.types.InputTextMessageContent(language_Vocabluary[language_Name]["inline_Messages"]["errors"]["nowPlaying_Nothing"]["description"]),
    description=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["nowPlaying_Nothing"]["description"])

    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=[results], cache_time=0)



def inline_Unknown_Error(inline_ID, language_Name):
    """
    ИНЛАЙН ОТВЕТ

    Ошибка "Неизвестная ошибка"
    """
    results = telebot.types.InlineQueryResultArticle(1,
    title=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["unknown_Error"]["title"],
    input_message_content=telebot.types.InputTextMessageContent(language_Vocabluary[language_Name]["inline_Messages"]["errors"]["unknown_Error"]["description"]),
    description=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["unknown_Error"]["description"])

    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=[results], cache_time=0)



def inline_Spotify_Not_Authorized(inline_ID, language_Name):
    """
    ИНЛАЙН ОТВЕТ

    Ошибка "Аккаунт Spotify не авторизован"
    """
    results = telebot.types.InlineQueryResultArticle(1,
    title=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["spotify_Not_Authorized"]["title"],
    input_message_content=telebot.types.InputTextMessageContent(language_Vocabluary[language_Name]["inline_Messages"]["errors"]["spotify_Not_Authorized"]["description"]),
    description=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["spotify_Not_Authorized"]["description"])

    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=[results], cache_time=0)



def inline_Auth_Error(inline_ID, language_Name):
    """
    ИНЛАЙН ОТВЕТ

    Ошибка "Ошибка авторизации Spotify аккаунта"
    """
    results = telebot.types.InlineQueryResultArticle(1,
    title=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["oauth_Error"]["title"],
    input_message_content=telebot.types.InputTextMessageContent(language_Vocabluary[language_Name]["inline_Messages"]["errors"]["oauth_Error"]["description"]),
    description=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["oauth_Error"]["description"])

    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=[results], cache_time=0)



def inline_No_Context(inline_ID, language_Name):
    """
    ИНЛАЙН ОТВЕТ

    Ошибка "Невозможно получить контекст"
    """
    results = telebot.types.InlineQueryResultArticle(1,
    title=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["no_Playback_Context"]["title"],
    input_message_content=telebot.types.InputTextMessageContent(language_Vocabluary[language_Name]["inline_Messages"]["errors"]["no_Playback_Context"]["description"]),
    description=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["no_Playback_Context"]["description"])

    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=[results], cache_time=0)



def inline_Private_Session(inline_ID, language_Name):
    """
    ИНЛАЙН ОТВЕТ

    Ошибка "Активна приватная сессия"
    """
    results = telebot.types.InlineQueryResultArticle(1,
    title=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["private_Session_Enabled"]["title"],
    input_message_content=telebot.types.InputTextMessageContent(language_Vocabluary[language_Name]["inline_Messages"]["errors"]["private_Session_Enabled"]["description"]),
    description=language_Vocabluary[language_Name]["inline_Messages"]["errors"]["private_Session_Enabled"]["description"])

    spotify_Bot.answer_inline_query(inline_query_id=inline_ID, results=[results], cache_time=0)
