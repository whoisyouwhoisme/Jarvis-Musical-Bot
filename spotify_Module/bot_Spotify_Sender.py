import telebot
import logging
import time
import json
import urllib

with open("bot_Keys.json") as json_File:
    bot_Keys_File = json.load(json_File)

spotify_Bot = telebot.TeleBot(bot_Keys_File["telegram"]["telegram_Key"])



def spotify_Login_Offer(chat_id, spotify_Auth_Link):
    """
    Просьба о входе в аккаунт Spotify
    """
    login_Keyboard = telebot.types.InlineKeyboardMarkup()
    login_Button = telebot.types.InlineKeyboardButton(text="Authorize on Spotify", url=spotify_Auth_Link)
    login_Keyboard.add(login_Button)
    spotify_Bot.send_message(chat_id, "Hi, i'm *Jarvis*, Your personal Spotify music bot. \n\nIt seems you are not signed in to your *Spotify* account. Please log in to your account. \n\n*You can disconnect your account at any time using the /logout command.*", parse_mode="Markdown", reply_markup=login_Keyboard)



def user_Leaving(chat_id):
    """
    Уведомление пользователю об успешном выходе из бота
    """
    disable_Keyboard = telebot.types.InlineKeyboardMarkup()
    disable_Button = telebot.types.InlineKeyboardButton(text="Disable Jarvis on Spotify Website", url="https://www.spotify.com/account/apps/")
    disable_Keyboard.add(disable_Button)
    spotify_Bot.send_message(chat_id, "I'm sorry that you are leaving. 😭 \nIf you have any problems, you can contact us via the /contacts command. \n\n*To completely disable the Jarvis, go to the Spotify website.*", parse_mode="Markdown", reply_markup=disable_Keyboard)



def auth_Complete(chat_id, user_Nickname):
    """
    Успешная авторизация
    """
    spotify_Bot.send_message(chat_id, f"Welcome aboard, *{user_Nickname}!* \n\nYour *Spotify* account is successfully connected! \n\n*Some useful commands:* \n*/menu* - Return to main menu \n*/logout* - Disable bot for your account \n*/contacts* - Contacts for communication with the developer \n\nEnjoy the bot. \nIf you have any questions, you can contact the developer.", parse_mode="Markdown")



def send_Developer_Contacts(chat_id):
    """
    Отправить контакты разработчика
    """
    links_Keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    discord_Button = telebot.types.InlineKeyboardButton(text="Discord", url="https://discord.gg/Z4A4qdw")
    vk_Button = telebot.types.InlineKeyboardButton(text="VK", url="https://vk.com/koteyk0o")
    links_Keyboard.add(discord_Button, vk_Button)
    spotify_Bot.send_message(chat_id, "Are you having problems? Questions? You found a bug? \n\nThere are 2 ways to contact the developer. *Discord* and *VKontakte*.", parse_mode="Markdown", reply_markup=links_Keyboard)    



def superShuffle_Description(chat_id):
    """
    Описание функции супер-шаффл
    """
    spotify_Bot.send_message(chat_id, "Due to unknown reasons, the shuffle in *Spotify* is sometimes not random. \n\nThe *Super Shuffle* takes all the songs from your *Liked Songs* section and just shuffles them so many times and then creates a new playlist where it puts those songs. \n\n*The minimum number of songs in the Liked Songs section should be 100.*", parse_mode="Markdown")



def yourTops_Description(chat_id):
    """
    Описание функции ваши-топы
    """
    spotify_Bot.send_message(chat_id, "In this section, you can find your *Top Artists*, and your *Top Songs* for a certain period of time. \n\nFor the *Top Songs*, I can suggest you create a playlist from these songs.", parse_mode="Markdown")



def controls_Main_Menu(chat_id):
    """
    Клавиатура основного меню
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    keyboard.row("Now Playing", "Super Shuffle")
    keyboard.row("Your Tops", "Other")
    spotify_Bot.send_message(chat_id, "Choose category", reply_markup=keyboard)



def other_Menu(chat_id):
    """
    Клавиатура остальных функций
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    keyboard.row("YouTube Clip")
    keyboard.row("Music Quiz")
    keyboard.row("Back to Menu")
    spotify_Bot.send_message(chat_id, "Choose category", reply_markup=keyboard)



def send_MusicQuiz_Round(chat_id, musicQuiz_Round_Data):
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

    spotify_Bot.send_audio(chat_id, audio=audio_File, title=audio_Title, caption="Listen the song, and select an answer 🤔", reply_markup=keyboard)



def musicQuiz_Rules(chat_id):
    """
    Отправить пользователю правила игры в музыкальную викторину
    """
    spotify_Bot.send_message(chat_id, "The *Music Quiz* consists of 10 songs from your music library. \n\n*Rules of the game:* \n1. You are given a 30 second segment of a song. \n2. You are given 10 seconds to answer, if you did not answer in time - the answer will be considered incorrect. \n3. You are given four choices, one of which is correct. \n4. Don't cheat! 🤔 \n\nYou can exit the game by entering the command */menu*", parse_mode="Markdown")



def shuffle_Tracks_Count(chat_id):
    """
    Вопрос пользователю о количестве треков для супер-шаффла
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=4)
    keyboard.row("100 Tracks", "200 Tracks", "All Tracks", "Back to Menu")
    spotify_Bot.send_message(chat_id, "How many songs should I add to the playlist?", reply_markup=keyboard)



def tops_Type_Select(chat_id):
    """
    Вопрос пользователю о типе топа
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3)
    keyboard.row("Tracks", "Artists", "Back to Menu")
    spotify_Bot.send_message(chat_id, "Which Top do you want to see?", reply_markup=keyboard)



def tops_Time_Period(chat_id):
    """
    Вопрос пользователю о периоде выборки для топа
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3)
    keyboard.row("4 Weeks", "6 Months", "All Time")
    spotify_Bot.send_message(chat_id, "Over what period of time?", reply_markup=keyboard)



def musicQuiz_Type_Select(chat_id):
    """
    Вопрос пользователю о выборке для викторины
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    keyboard.row("Liked Songs", "Top Tracks")
    spotify_Bot.send_message(chat_id, "Select a quiz section", reply_markup=keyboard)



def tracks_Top(chat_id, top_Data):
    """
    Вывод топа песен пользователя
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    keyboard.row("Yes, Create Playlist", "No, Thanks")

    chat_Top_Data = {}
    chat_Top_Data["header"] = "Here's your top songs <b>(Displayed only 10 songs out of 50)</b>:" + "\n\n"
    chat_Top_Data["footer"] = "\n" + "Do I need to create a playlist? <b>(The playlist will contain 50 songs)</b>"

    chat_Top_Data["top_Summary"] = chat_Top_Data["header"]

    for top_Item in range(10):
        artists = top_Data[top_Item]["artists"]
        name = top_Data[top_Item]["name"]
        chat_Top_Data[top_Item] = f"<b>{top_Item + 1}.</b> {artists} - {name} \n\n"
        chat_Top_Data["top_Summary"] += chat_Top_Data[top_Item]

    chat_Top_Data["top_Summary"] += chat_Top_Data["footer"]
    spotify_Bot.send_message(chat_id, chat_Top_Data["top_Summary"], reply_markup=keyboard, parse_mode="HTML")



def artists_Top(chat_id, top_Data):
    """
    Вывод топа исполнителей пользователя
    """
    chat_Top_Data = {}
    chat_Top_Data["top_Summary"] = "Here's your top artists <b>(Displayed only 10 artists out of 50)</b>:" + "\n\n"

    for top_Item in range(10):
        name = top_Data[top_Item]["name"]
        followers = top_Data[top_Item]["followers"]
        chat_Top_Data[top_Item] = f"<b>{top_Item + 1}.</b> {name} - {followers} Followers \n\n"
        chat_Top_Data["top_Summary"] += chat_Top_Data[top_Item]

    spotify_Bot.send_message(chat_id, chat_Top_Data["top_Summary"], parse_mode="HTML")



def astray_Notification(chat_id):
    """
    Сообщить пользователю о возможности вызова клавиатуры
    """ 
    spotify_Bot.send_message(chat_id, "If you suddenly get astray, you can use the */menu* command to return to the main menu.", parse_mode="Markdown")



def insufficient_Data_For_Top(chat_id):
    """
    Не хватает песен для составления топа
    """
    spotify_Bot.send_message(chat_id, "*Not enough data to display the tops.* \n\nListen to the songs more often, and someday the data will appear.", parse_mode="Markdown")



def now_Playing_Error(chat_id):
    """
    Недостаточно метаданных для отображения
    """
    spotify_Bot.send_message(chat_id, "*This song does not contain all the metadata*, so the information cannot be displayed.", parse_mode="Markdown")



def search_Clip(chat_id):
    """
    Клип в процессе поиска
    """
    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    spotify_Bot.send_message(chat_id, "*Your clip is being searched*, please wait.", reply_markup=markup, parse_mode="Markdown")



def musicQuiz_Preparing(chat_id):
    """
    Игровая сессия подготавливается
    """
    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    spotify_Bot.send_message(chat_id, "*Your game session is being prepared*, please wait.", reply_markup=markup, parse_mode="Markdown")



def musicQuiz_Incorrect_Answer(chat_id, musicQuiz_Round_Stats):
    """
    Неправильный ответ викторины
    """

    right_Answer = musicQuiz_Round_Stats["round_Answer"]
    took_Time_Answer = int(time.time()) - musicQuiz_Round_Stats["round_Prepared_Timestamp"]
    message_Text = f"🔴 <b>Unfortunately, no!<b> \n\nThis is: <b>{right_Answer}<b> \n\nAnswer Time: <b>{took_Time_Answer}s<b>"

    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    spotify_Bot.send_message(chat_id, message_Text, reply_markup=markup, parse_mode="HTML")



def musicQuiz_Correct_Answer(chat_id, musicQuiz_Round_Stats):
    """
    Правильный ответ викторины
    """

    right_Answer = musicQuiz_Round_Stats["round_Answer"]
    took_Time_Answer = int(time.time()) - musicQuiz_Round_Stats["round_Prepared_Timestamp"]
    message_Text = f"🟢 <b>Great!<b> \n\nThis is: <b>{right_Answer}<b> \n\nAnswer Time: <b>{took_Time_Answer}s<b>"

    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    spotify_Bot.send_message(chat_id, message_Text, reply_markup=markup, parse_mode="HTML")



def musicQuiz_Answer_Timeout(chat_id, musicQuiz_Round_Stats):
    """
    Закончилось время на ответ викторины
    """

    right_Answer = musicQuiz_Round_Stats["round_Answer"]
    took_Time_Answer = int(time.time()) - musicQuiz_Round_Stats["round_Prepared_Timestamp"]
    message_Text = f"🔴 <b>Unfortunately, the time to answer the question has run out!<b> \n\nThis is: <b>{right_Answer}<b> \n\nAnswer Time: <b>{took_Time_Answer}s<b>"

    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    spotify_Bot.send_message(chat_id, message_Text, reply_markup=markup, parse_mode="HTML")



def musicQuiz_End(chat_id, musicQuiz_Statistic):
    """
    Конец музыкальной викторины
    """
    markup = telebot.types.ReplyKeyboardRemove(selective=False)

    total_Rounds = musicQuiz_Statistic["total_Rounds"]
    correct_Answers = musicQuiz_Statistic["correct_Answers"]
    message_Text = f"*The quiz is over!* \n\nYour Result Is *{correct_Answers} / {total_Rounds}*"
    spotify_Bot.send_message(chat_id, message_Text, reply_markup=markup, parse_mode="Markdown")



def musicQuiz_Error_NoTracks(chat_id):
    """
    Ошибка MusicQuiz - не хватило треков для начала игры
    """
    spotify_Bot.send_message(chat_id, "Due to the peculiarities of *Spotify*, could not create a game session.\n\n *Please try again*.", parse_mode="Markdown")



def musicQuiz_Error_RoundProcess(chat_id):
    """
    Ошибка MusicQuiz - возникла ошибка при обработке раунда
    """
    spotify_Bot.send_message(chat_id, "*Sorry*, Music Quiz has encountered an internal error.\n\n *Try to start a new game*.", parse_mode="Markdown")



def insufficient_Data_For_Shuffle(chat_id):
    """
    Недостаточно песен для супер-шаффла
    """
    spotify_Bot.send_message(chat_id, "*You don't have enough songs for Super Shuffle.* \n\nAdd more songs and this feature will be available (minimum 200 songs)", parse_mode="Markdown")



def insufficient_Data_For_MusicQuiz(chat_id):
    """
    Недостаточно песен для музыкальной викторины
    """
    spotify_Bot.send_message(chat_id, "*You don't have enough songs for Music Quiz.* \n\nListen to more songs, and someday you can play a Music Quiz.", parse_mode="Markdown")



def nowplaying_Nothing(chat_id):
    """
    В данный момент ничего не играет
    """
    spotify_Bot.send_message(chat_id, "At the moment, nothing is playing.", parse_mode="Markdown")



def cannot_Authorize(chat_id):
    """
    Ошибка авторизации пользователя
    """
    spotify_Bot.send_message(chat_id, "*I cannot authorize you on Spotify.* \n\nMaybe you have blocked the bot in your *Spotify* account, use the /logout command and log in again.", parse_mode="Markdown")



def servers_Link_Error(chat_id):
    """
    Ошибка связи с серверами Спотифая
    """
    spotify_Bot.send_message(chat_id, "Unable to connect to *Spotify* servers. \n\nPerhaps this is *Spotify* server error, and you need to wait.", parse_mode="Markdown")



def unknown_Error(chat_id):
    """
    Неизвестная ошибка
    """
    spotify_Bot.send_message(chat_id, "*Unknown error.* If the error persists, contact the developer via the */contacts* command", parse_mode="Markdown")



def denied_Work_Reason(chat_id):
    """
    Пока выполняется работа, вы не можете использовать эту функцию
    """
    spotify_Bot.send_message(chat_id, "At the moment, you can not use this function, please wait.", parse_mode="Markdown")



def playlist_Preparing(chat_id):
    """
    Плейлист готовится
    """
    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    spotify_Bot.send_message(chat_id, "*Your playlist is being prepared, please wait.* It might take a couple of minutes.", reply_markup=markup, parse_mode="Markdown")



def function_On_Way(chat_id):
    """
    Функция скоро появится
    """
    spotify_Bot.send_message(chat_id, "This feature will be available soon, stay tuned.", parse_mode="Markdown")



def playlist_Ready(chat_id, playlist_Data):
    """
    Плейлист готов
    """
    playlist_Keyboard = telebot.types.InlineKeyboardMarkup()
    playlist_Button = telebot.types.InlineKeyboardButton(text="Open on Spotify", url=playlist_Data["external_URL"])
    playlist_Keyboard.add(playlist_Button)

    ready_Data = {}
    ready_Data["name"] = "<b>Name:</b> " + playlist_Data["name"] + "\n"
    ready_Data["description"] = "<b>Description:</b> " + playlist_Data["description"] + "\n"
    ready_Data["total_Tracks"] = "<b>Tracks:</b> " + str(playlist_Data["total_Tracks"]) + "\n"
    ready_Data["playlist_Summary"] = ready_Data["name"] + ready_Data["description"] + ready_Data["total_Tracks"]

    ready_Text = "Your playlist is ready!" + "\n\n" + ready_Data["playlist_Summary"]
    playlist_Cover = urllib.request.urlopen(playlist_Data["image_URL"]).read()

    spotify_Bot.send_photo(chat_id, playlist_Cover, caption=ready_Text, reply_markup=playlist_Keyboard, parse_mode="HTML")



def now_Playing(chat_id, playing_Data):
    """
    Вывод сейчас играет
    """
    now_Playing_Data = {}
    now_Playing_Data["artists"] = "<b>Artist:</b> " + ", ".join(playing_Data["artists"]) + "\n"
    now_Playing_Data["album_Name"] = "<b>Album:</b> " + playing_Data["album_Name"] + "\n"
    now_Playing_Data["song_Name"] = "<b>Song:</b> " + playing_Data["song_Name"] + "\n"
    now_Playing_Data["song_Duration"] = "<b>Duration:</b> " + time.strftime("%M:%S", time.gmtime(playing_Data["song_Duration"] / 1000)) + "\n"
    now_Playing_Data["playback_Summary"] = now_Playing_Data["song_Name"] + now_Playing_Data["artists"] + now_Playing_Data["album_Name"] + now_Playing_Data["song_Duration"]

    playback_Text = "Now playing:" + "\n\n" + now_Playing_Data["playback_Summary"]
    playback_Cover = urllib.request.urlopen(playing_Data["song_Cover_URL"]).read()

    spotify_Bot.send_photo(chat_id, playback_Cover, caption=playback_Text, parse_mode="HTML")



def clip_Message(chat_id, playing_Data):
    """
    Вывод клипа
    """
    now_Playing_Data = {}
    now_Playing_Data["artists"] = "<b>Artist:</b> " + ", ".join(playing_Data["artists"]) + "\n"
    now_Playing_Data["song_Name"] = "<b>Song:</b> " + playing_Data["song_Name"] + "\n\n"
    now_Playing_Data["youtube_Clip_Link"] = playing_Data["youtube_URL"]
    now_Playing_Data["playback_Summary"] = now_Playing_Data["artists"] + now_Playing_Data["song_Name"] + now_Playing_Data["youtube_Clip_Link"]

    playback_Text = "Now playing:" + "\n\n" + now_Playing_Data["playback_Summary"]

    spotify_Bot.send_message(chat_id, text=playback_Text, parse_mode="HTML")