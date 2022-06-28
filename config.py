import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# configuration from .ENV file
BOT_HASH = os.environ.get("BOT_HASH")
OPEN_WEATHER_API_KEY=os.environ.get("OPEN_WEATHER_API_KEY")
GEOCODING_API_KEY=os.environ.get("GEOCODING_API_KEY")
METEOMATICS_USERNAME=os.environ.get("METEOMATICS_USERNAME")
METEOMATICS_PASSWORD=os.environ.get("METEOMATICS_PASSWORD")

# local configuration related to the application
APP_DB_NAME = "app_db.db"
WEATHER_CACHE_TABLE_NAME = "weather_cache"
USER_OPTIONS_TABLE_NAME = "user_options"
