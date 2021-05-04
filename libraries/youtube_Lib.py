import requests
import json
import os
import googleapiclient.discovery

with open("bot_Keys.json") as bot_Keys_File:
    bot_Keys = json.load(bot_Keys_File)

API_Key = bot_Keys["google"]["youTube_Key"]

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=API_Key)

def search_Youtube(keywords):
    """
    Search YouTube videos by keywords

    keywords - a string of keywords
    """
    request = youtube.search().list(
        part="snippet",
        maxResults=5,
        q=keywords,
    )

    response = request.execute()

    return response