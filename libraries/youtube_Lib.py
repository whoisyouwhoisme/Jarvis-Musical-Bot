import requests
import json
import os
import googleapiclient.discovery

with open("bot_Keys.json") as json_File:
    bot_Keys_File = json.load(json_File)

API_Key = bot_Keys_File["google"]["youTube_Key"]

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=API_Key)

def search_Youtube(keywords):
    """
    Поиск видео в YouTube по ключевым словам

    keywords - строка из ключевых слов
    """
    request = youtube.search().list(
        part="snippet",
        maxResults=5,
        q=keywords,
    )

    response = request.execute()

    return response