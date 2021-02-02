import telebot
import json
from spotify_Module import bot_Spotify_Module
from spotify_Module import bot_Inline_Handler
from spotify_Module import bot_Callback_Handler

with open("bot_Keys.json") as json_File:
    bot_Keys_File = json.load(json_File)

spotify_Bot = telebot.TeleBot(bot_Keys_File["telegram"]["telegram_Key"])



@spotify_Bot.callback_query_handler(func=lambda call: True) #Слушатель callback кнопок
def get_Callback_Data(call):
    bot_Callback_Handler.process_Callback_Data(call)

@spotify_Bot.inline_handler(func=lambda query: len(query.query) > 0) #Слушатель Inline режима
def get_Inline_Data(query):
    bot_Inline_Handler.process_Inline_Data(query)

@spotify_Bot.message_handler(commands=["logout"]) #Слушатель команды Logout
def logout_Command_Handler(message):
    bot_Spotify_Module.logout_Command(message)

@spotify_Bot.message_handler(commands=["menu"]) #Слушатель команды Menu
def menu_Command_Handler(message):
    bot_Spotify_Module.menu_Command(message)

@spotify_Bot.message_handler(commands=["language"]) #Слушатель команды Language
def language_Command_Handler(message):
    bot_Spotify_Module.language_Command(message)

@spotify_Bot.message_handler(commands=["contacts"]) #Слушатель команды Contacts
def contacts_Command_Handler(message):
    bot_Spotify_Module.contacts_Command(message)

@spotify_Bot.message_handler(content_types=["text"]) #Слушатель текстовых сообщений
def get_Text_Message(message):
    bot_Spotify_Module.chat_Messages_Handler(message)
    print("ID: ", message.from_user.id, " Message: ", message.text)



print("Mothership launched!")



def proceed_Updates(json_Updates):
    update = telebot.types.Update.de_json(json_Updates)
    spotify_Bot.process_new_updates([update])