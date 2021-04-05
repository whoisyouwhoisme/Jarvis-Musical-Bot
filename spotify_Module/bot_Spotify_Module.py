"""
Ребята не стоит вскрывать этот код. 
Вы молодые, шутливые, вам все легко. Это не то. Это не Stuxnet и даже не шпионские программы ЦРУ. Сюда лучше не лезть. 
Серьезно, любой из вас будет жалеть. 
Лучше закройте код и забудьте что там писалось. 
Я вполне понимаю что данным сообщением вызову дополнительный интерес, но хочу сразу предостеречь пытливых - стоп. Остальные просто не найдут.
"""

import time

from spotify_Module import localization
from spotify_Module import bot_Sender

from spotify_Module import bot_SuperShuffle
from spotify_Module import bot_LibraryTops
from spotify_Module import bot_MusicQuiz
from spotify_Module import bot_Player_Control
from spotify_Module import bot_BlockedTracks
from spotify_Module import bot_LibraryStatistics

from spotify_Module.spotify_Logger import logger
from libraries import spotify_Oauth
from libraries import database_Manager as db_Manager

bot_Version = 0.4

language_Vocabluary = localization.load_Vocabluary()



def to_Main_Menu(user_ID):
    """
    Вернуть пользователя в главное меню
    """
    logger.info(f"Sending Main Menu Keyboard For User {user_ID}")
    db_Manager.write_User_Position(user_ID, "main_Menu")
    user_Language = db_Manager.get_User_Language(user_ID)
    bot_Sender.controls_Main_Menu(user_ID, language_Name=user_Language)



def process_User_Language(language_Code):
    if language_Code == "ru" or language_Code == "uk" or language_Code == "be": #Русский, украинский, беларусский
        user_Language = "RUS"
    else:
        user_Language = "ENG"
    
    return user_Language



def logout_Command(message):
    """
    Обработка команды выхода

    Удаление пользователя из всех таблиц в базе данных
    """
    user_ID = message.from_user.id
    if db_Manager.check_Bot_Reg(user_ID):
        logger.info(f"Preparing Logout For User {user_ID}")
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)
        user_Language = db_Manager.get_User_Language(user_ID)
        
        db_Manager.delete_User(user_Unique_ID, "bot_Users")
        db_Manager.delete_User(user_Unique_ID, "spotify_Users")
        db_Manager.delete_User(user_Unique_ID, "users_TopTracks")
        db_Manager.delete_User(user_Unique_ID, "users_TopArtists")

        logger.info(f"Logout Successful For User {user_ID}")
        bot_Sender.user_Leaving(message.from_user.id, language_Name=user_Language)



def language_Command(message):
    """
    Обработка команды смены языка
    """
    user_ID = message.from_user.id
    if db_Manager.check_Spotify_Login(user_ID):
        logger.info(f"Sending Language Selector Keyboard For User {user_ID}")
        user_ID = message.from_user.id
        bot_Sender.language_Selector(user_ID, db_Manager.get_User_Language(user_ID))
        db_Manager.write_User_Position(user_ID, "language_Select")



def menu_Command(message):
    """
    Обработка команды меню

    Если пользователь авторизован, вернуть его в главное меню
    """
    user_ID = message.from_user.id

    if db_Manager.check_Spotify_Login(user_ID):
        to_Main_Menu(user_ID)



def contacts_Command(message):
    """
    Обработка команды контактов

    Отправить пользователю контакты разработчика
    """
    user_ID = message.from_user.id

    logger.info(f"Sending Contacts For User {user_ID}")
    user_Language = db_Manager.get_User_Language(user_ID)
    bot_Sender.send_Developer_Contacts(user_ID, language_Name=user_Language)



logger.info("Spotify Module Ready")




def chat_Messages_Handler(message):
    user_ID = message.from_user.id
    logger.info(f"New Message: {message.text} From: {user_ID}")

    if not db_Manager.check_Bot_Reg(user_ID): #Если в базе данных его нет, регистрируем
        generated_Unique_ID = db_Manager.generate_Unique_ID()
        user_LanguageCode = message.from_user.language_code

        user_FirstName = message.from_user.first_name
        user_UserName = message.from_user.username
        user_LastName = message.from_user.last_name

        reg_Timestamp = int(time.time())

        logger.info(f"User {user_ID} ({user_FirstName}, {user_LastName}, {user_UserName}) Not In Reg Table. Registration...")
        db_Manager.register_User(user_ID, generated_Unique_ID, process_User_Language(user_LanguageCode), bot_Version, reg_Timestamp)



    #Оптимизация для БД
    user_Position_Cache = db_Manager.get_User_Position(user_ID) #Записать в переменную позицию пользователя
    user_Language = db_Manager.get_User_Language(user_ID) #Записать в переменную язык пользователя



    if not db_Manager.check_Spotify_Login(user_ID): #Если пользователь еще не вошел в Spotify, предлагаем войти
        logger.info(f"User {user_ID} Not In Spotify Table. Sending Offer For Login")
        user_Unique_ID = db_Manager.get_User_UniqueID(user_ID)
        spotify_Auth_Link = spotify_Oauth.generate_Auth_Link(user_Unique_ID)
        bot_Sender.spotify_Login_Offer(user_ID, spotify_Auth_Link, language_Name=user_Language)



    if db_Manager.check_Spotify_Login(user_ID):
        logger.info(f"User {user_ID} Have Spotify Login")


        #Заглушка если in Work позиция
        if user_Position_Cache == "work_In_Progress":
            bot_Sender.denied_Work_Reason(user_ID, language_Name=user_Language)


        #Меню смены языка
        if user_Position_Cache == "language_Select":
            if message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["language"]["ENG"]:
                db_Manager.write_User_Language(user_ID, "ENG")
                bot_Sender.language_Changed(user_ID, "ENG")
                to_Main_Menu(user_ID)

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["language"]["RUS"]:
                db_Manager.write_User_Language(user_ID, "RUS")
                bot_Sender.language_Changed(user_ID, "RUS")
                to_Main_Menu(user_ID)
            
            else:
                bot_Sender.astray_Notification(user_ID, db_Manager.get_User_Language(user_ID))


        if db_Manager.get_User_BotVersion(user_ID) < bot_Version: #Если версия клавиатуры пользователя старая, то перемещаем в главное меню
            to_Main_Menu(user_ID)
            bot_Sender.jarvis_Updated(user_ID, language_Name=user_Language, jarvis_Version=bot_Version)
            db_Manager.write_User_BotVersion(user_ID, bot_Version)


        #ГЛАВНОЕ МЕНЮ


        if user_Position_Cache == "main_Menu":
            if message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["inline_Help"]: #Пункт Inline Help
                logger.info(f"Sending Inline Help for user {user_ID}")
                bot_Sender.inline_Mode_Help(user_ID, language_Name=user_Language)

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["super_Shuffle"]: #Пункт Супер-шаффла
                logger.info(f"User {user_ID} Entered To Super Shuffle")
                db_Manager.write_User_Position(user_ID, "user_SuperShuffle")
                bot_Sender.superShuffle_Description(user_ID, language_Name=user_Language)
                bot_Sender.shuffle_Tracks_Count(user_ID, language_Name=user_Language)
                logger.info(f"Sending Super Shuffle Selector For User {user_ID}")

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["your_Tops"]: #Пункт топов
                logger.info(f"User {user_ID} Entered To Your Tops")
                db_Manager.write_User_Position(user_ID, "user_YourTops")
                bot_Sender.yourTops_Description(user_ID, language_Name=user_Language)
                bot_Sender.tops_Type_Select(user_ID, language_Name=user_Language)
                logger.info(f"Sending Your Tops Selector For User {user_ID}")
            
            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["musicQuiz"]: #Пункт музыкальной викторины
                logger.info(f"User {user_ID} Entered To Music Quiz")
                db_Manager.write_User_Position(user_ID, "user_MusicQuiz_Type")
                bot_Sender.musicQuiz_Rules(user_ID, language_Name=user_Language)
                bot_Sender.musicQuiz_Type_Select(user_ID, language_Name=user_Language)
                logger.info(f"Sending Music Quiz Type Selector For User {user_ID}")

            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["blocked_Tracks"]: #Пункт заблокированных треков
                logger.info(f"User {user_ID} Entered To Blocked Tracks")
                db_Manager.write_User_Position(user_ID, "user_BlockedTracks")
                bot_Sender.blocked_Tracks_Description(user_ID, language_Name=user_Language)
                bot_BlockedTracks.send_BlockedTracks(user_ID, language_Name=user_Language)
            
            elif message.text == language_Vocabluary[user_Language]["keyboard_Buttons"]["menu_Buttons"]["library_Statistics"]: #Пункт статистики
                logger.info(f"User {user_ID} Entered To Library Statistics")
                db_Manager.write_User_Position(user_ID, "user_LibraryStatistics_Type")
                bot_Sender.library_Statistics_Description(user_ID, language_Name=user_Language)
                bot_Sender.library_Statistics_Type(user_ID, language_Name=user_Language)
                logger.info(f"Sending Statistics Type Selector For User {user_ID}")

            else:
                if message.content_type == "photo": #СПАСИБО КИРЮШЕ ЗА ПАСХАЛКУ
                    bot_Sender.send_Easter_Egg(user_ID, language_Vocabluary[user_Language]["chat_Messages"]["easter_Eggs"]["britt_Robertson"])
                
                else:
                    message_Text = message.text.lower()
                
                    if message_Text == "42":
                        bot_Sender.send_Easter_Egg(user_ID, language_Vocabluary[user_Language]["chat_Messages"]["easter_Eggs"]["42"])
                        bot_Player_Control.start_Playback("track", "7qXddTDsEuxInJ8jzX1D9a", user_ID=user_ID, user_Language=user_Language)

                    elif message_Text == "tears in rain":
                        bot_Sender.send_Easter_Egg(user_ID, language_Vocabluary[user_Language]["chat_Messages"]["easter_Eggs"]["blade_Runner"])
                        bot_Player_Control.start_Playback("track", "2LxEIWrZkzfc55c3rk05DH", user_ID=user_ID, user_Language=user_Language)

                    elif message_Text == "grogu":
                        bot_Player_Control.start_Playback("track", "0PqdMQecGbrFd2c35l4ROS", user_ID=user_ID, user_Language=user_Language)

                    elif message_Text == "the oa":
                        bot_Player_Control.start_Playback("track", "0wokCRaKD0zPNhMRXAgVsr", user_ID=user_ID, user_Language=user_Language)                                        

                    else:
                        bot_Sender.astray_Notification(user_ID, language_Name=user_Language)


        #ПУНКТ СУПЕР-ШАФФЛА


        if user_Position_Cache == "user_SuperShuffle":
            bot_SuperShuffle.process_SuperShuffle_Message(user_ID, message_Text=message.text, user_Language=user_Language)


        #ПУНКТ ТОПОВ

        if user_Position_Cache == "user_YourTops":
            bot_LibraryTops.process_Type_Selector_Message(user_ID, message_Text=message.text, user_Language=user_Language)

        if user_Position_Cache == "user_TopTracks_Time":
            bot_LibraryTops.process_TopSongs_Time_Selector_Message(user_ID, message_Text=message.text, user_Language=user_Language)

        if user_Position_Cache == "user_TopArtists_Time":
            bot_LibraryTops.process_TopArtists_Time_Selector_Message(user_ID, message_Text=message.text, user_Language=user_Language)


        #ПУНКТ МУЗЫКАЛЬНОЙ ВИКТОРИНЫ


        if user_Position_Cache == "user_MusicQuiz_Type":
            bot_MusicQuiz.process_Type_Selector_Message(user_ID, message_Text=message.text, user_Language=user_Language)

        if user_Position_Cache == "user_MusicQuiz_Time":
            bot_MusicQuiz.process_Time_Selector_Message(user_ID, message_Text=message.text, user_Language=user_Language)
        
        if user_Position_Cache == "user_MusicQuiz_inGame":
            bot_MusicQuiz.process_InGame_Message(user_ID, message_Text=message.text, user_Language=user_Language)
        

        #Пункт статистики
        if user_Position_Cache == "user_LibraryStatistics_Type":
            bot_LibraryStatistics.process_Type_Selector_Message(user_ID, message_Text=message.text, user_Language=user_Language)
