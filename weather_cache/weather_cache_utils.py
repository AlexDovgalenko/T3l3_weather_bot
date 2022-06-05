import logging
import sqlite3
from typing import Optional

from config import APP_DB_NAME, WEATHER_CACHE_TABLE_NAME
from geocoding.geocoding_exceptions import GeneralGeocodingError, UnableToLocateCoordinates
from geocoding.geocoding_utils import get_lat_lon_from_city_name
from weather_cache.weather_cache_exceptions import FailedToCheckWeatherCache, FailedToGetWeatherDataFromDB, \
    FailedToInsertWeatherDataIntoDB, FailedToUpdateWeatherDataInDB, FailedToUpdateWeatherCache

# load_dotenv(find_dotenv())

# APP_DB_NAME = os.environ.get("APP_DB_NAME")
# WEATHER_CACHE_TABLE_NAME = os.environ.get("WEATHER_CACHE_TABLE_NAME")

# APP_DB_NAME = "weather_cache/weather_cache.db"
# WEATHER_CACHE_TABLE_NAME = "weather_cache"

logger = logging.getLogger()


class WeatherCacheDB:
    f"""Class to initialize SQLite db instance and creates weather cache file '{APP_DB_NAME}' if it is absent.
     Also it creates table with name '{WEATHER_CACHE_TABLE_NAME}' in case if it absent."""

    def __init__(self, db_name):
        self._db_connection = sqlite3.connect(db_name, check_same_thread=False)
        self._db_cursor = self._db_connection.cursor()
        result_query = self._db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        # creates a table in case if it is absent
        if not result_query or WEATHER_CACHE_TABLE_NAME not in sorted(list(zip(*result_query))[0]):
            self._db_cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS {WEATHER_CACHE_TABLE_NAME} (LAT_LON TEXT, WEATHER_PROVIDER TEXT, PERIOD TEXT, TIMESTAMP INTEGER, WEATHER_DATA 
                TEXT)""")
            self._db_connection.commit()

    @property
    def db_cursor(self):
        return self._db_cursor

    @property
    def db_connection(self):
        return self._db_connection


weather_db = WeatherCacheDB(APP_DB_NAME)


def get_weather_item_from_db(lat_lon: str, weather_provider_name: str, period: str):
    logger.info(f"Tryint to get weather data with lat-lon: '{lat_lon}', period: {period} and weather "
                f"provider: '{weather_provider_name}'...")
    try:
        sql_query = f"""SELECT * from {WEATHER_CACHE_TABLE_NAME} WHERE LAT_LON = '{lat_lon}' AND WEATHER_PROVIDER = '{weather_provider_name}' AND PERIOD = '{period}'"""
        weather_db.db_cursor.execute(sql_query)
        result = weather_db.db_cursor.fetchone()
    except Exception as err:
        logger.error(err)
        raise FailedToGetWeatherDataFromDB("Failed to get weather data from the DB.")
    return result


def insert_weather_item_into_db(weather_provider_name: str, timestamp: int, period: str, weather_data: str,
                                lat_lon: Optional[str], city_name: Optional[str] = None):
    if not lat_lon:
        lat_lon = "-".join(get_lat_lon_from_city_name(city_name))
    logger.info(f"Inserting weather data with lat-lon: '{lat_lon}', period: {period} and weather "
                f"provider: '{weather_provider_name}'...")
    try:
        sql_query = f"""INSERT into {WEATHER_CACHE_TABLE_NAME} values (?, ?, ?, ?, ?) """
        weather_db.db_cursor.execute(sql_query, (lat_lon, weather_provider_name, period, timestamp, weather_data))
        weather_db.db_connection.commit()
    except Exception as err:
        logger.error(err)
        raise FailedToInsertWeatherDataIntoDB("Failed to insert weather data into the DB.")


def update_weather_item_in_db(weather_provider_name: str, timestamp: int, period: str, weather_data: str, lat_lon: str):
    logger.info(f"Updating weather data with lat-lon: '{lat_lon}', period: '{period}' and weather "
                f"provider: '{weather_provider_name}'...")
    try:
        sql_query = f""" UPDATE {WEATHER_CACHE_TABLE_NAME} SET TIMESTAMP = {timestamp}, WEATHER_DATA = '{weather_data}' 
        WHERE LAT_LON = '{lat_lon}' AND  WEATHER_PROVIDER = '{weather_provider_name}' AND PERIOD = '{period}'"""
        weather_db.db_cursor.execute(sql_query)
        weather_db.db_connection.commit()
    except Exception as err:
        logger.error(err)
        raise FailedToUpdateWeatherDataInDB("Failed to update weather data in the DB.")


def check_weather_cache(city_name: str, weather_provider_name: str, timestamp: int, period: str):
    """Function checks if combination of city location + weather provider record already exists in DB, and it is more
     than one hour old.
     Returns """
    try:
        lat, lon = get_lat_lon_from_city_name(city_name)
    except (GeneralGeocodingError, UnableToLocateCoordinates):
        err = f"Unable to obtain Latutude and Lontitude for provided city '{city_name}'."
        logger.error(err)
        raise FailedToCheckWeatherCache(err)
    lat_lon = "-".join([lat, lon])
    try:
        result = get_weather_item_from_db(lat_lon=lat_lon, weather_provider_name=weather_provider_name, period=period)
    except FailedToCheckWeatherCache:
        err = f"Unable to fetch data for lat-lon: '{lat_lon}' and weather_provider_name: '{weather_provider_name}' " \
              f"from the Weathed Cache DB."
        logger.error(err)
        raise FailedToCheckWeatherCache(err)
    if not result:
        # TODO Raise appropriate exception here
        return False, None
    is_cache_actual = check_time_frame(db_timestamp=result[3], current_timestamp=timestamp)
    return is_cache_actual, result


def update_weather_cache(lat_lon: str, period: str, weather_provider_name: str, timestamp: int,
                         current_weather_data: str):
    try:
        result = get_weather_item_from_db(lat_lon=lat_lon, weather_provider_name=weather_provider_name, period=period)
        if result:
            if not check_time_frame(db_timestamp=result[3], current_timestamp=timestamp):
                update_weather_item_in_db(weather_provider_name=weather_provider_name, timestamp=timestamp,
                                          weather_data=current_weather_data, lat_lon=lat_lon, period=period)
        else:
            insert_weather_item_into_db(weather_provider_name=weather_provider_name, timestamp=timestamp,
                                        weather_data=current_weather_data, lat_lon=lat_lon, period=period)
    except FailedToCheckWeatherCache as err:
        logger.error(err)
        raise FailedToUpdateWeatherCache("Failed to update weather cache data in the DB.")


def check_time_frame(db_timestamp: int, current_timestamp: int):
    """Functions checks whether current time exceeds time from DB record for more than an hour."""
    return not (int(current_timestamp) - int(db_timestamp) > 3600)


if __name__ == '__main__':
    # get_weather_item_from_db()
    # insert_weather_item_into_db(city_name="Odesa",  weather_provider_name="Sinoptik", timestamp=1652527560, weather_data="Some Weather data237328")
    update_weather_item_in_db(lat_lon="46.472500000000025-30.73711000000003", weather_provider_name="Sinoptik",
                              timestamp=1652527777,
                              weather_data="Some Weather data 4444")
    # timestamp = int(datetime.now().timestamp())
    # print(get_weather_item_from_db('46.472500000000026-30.73711000000003', "Sinoptik"))
    # print(datetime.fromtimestamp(1652527516.639966))
    # print(datetime.from-timestamp(timestamp))
