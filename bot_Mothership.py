import telebot
import time
import json
from spotify_Module import bot_Spotify_Module

with open("bot_Keys.json") as json_File:
    bot_Keys_File = json.load(json_File)

spotify_Bot = telebot.TeleBot(bot_Keys_File["telegram"]["telegram_Key"])



@spotify_Bot.message_handler(commands=["logout"]) #Слушатель команды Logout
def logout_Command_Handler(message):
    bot_Spotify_Module.logout_Command(message)

@spotify_Bot.message_handler(commands=["menu"]) #Слушатель команды Menu
def menu_Command_Handler(message):
    bot_Spotify_Module.menu_Command(message)

@spotify_Bot.message_handler(commands=["contacts"]) #Слушатель команды Contacts
def contacts_Command_Handler(message):
    bot_Spotify_Module.contacts_Command(message)

@spotify_Bot.message_handler(content_types=["text"]) #Слушатель текстовых сообщений
def get_Text_Message(message):
    bot_Spotify_Module.chat_Messages_Handler(message)
    print("ID: ", message.from_user.id, " Message: ", message.text)

print("Mothership launched!")

spotify_Bot.polling(none_stop=True)