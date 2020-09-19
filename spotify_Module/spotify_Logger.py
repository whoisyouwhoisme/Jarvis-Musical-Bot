import logging
import os
import time

logger = logging
bot_Path = os.getcwd()
bot_Log_File_Path = bot_Path + "/logs/" + time.strftime("/spotify_Module-%Y-%m-%d.log")
logger.basicConfig(filename=bot_Log_File_Path, level=logging.INFO, format="%(asctime)s %(levelname)-12s %(message)s")