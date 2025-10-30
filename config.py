import asyncio
import logging
import sys
import os
import re
from enum import Enum
import requests
from pathlib import Path
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import urllib3
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile, InputMediaPhoto

load_dotenv()

CFG_CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
CFG_CHANNEL_MESSAGE_ID = int(os.getenv("CHANNEL_MESSAGE_ID"))

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    redirect_uri=os.getenv("REDIRECT_URI"),
    scope=os.getenv("SCOPE")
))

bot = Bot(token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))