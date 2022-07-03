import sqlite3
from typing import Tuple, Optional, Union

from loguru import logger

from config import APP_DB_NAME, WEATHER_CACHE_TABLE_NAME
from weather_cache.weather_cache_exceptions import FailedToCheckWeatherCache, FailedToGetWeatherDataFromDB, \
    FailedToInsertWeatherDataIntoDB, FailedToUpdateWeatherDataInDB, FailedToUpdateWeatherCache
from weather_providers.weather_provider_strategy import WeatherForecastType


class WeatherCacheDB:
    f"""Class to initialize SQLite db instance and creates weather cache file '{APP_DB_NAME}' if it is absent.
     Also it creates table with name '{WEATHER_CACHE_TABLE_NAME}' in case if it absent."""

    def __init__(self, db_name):
        self._db_connection = sqlite3.connect(db_name, check_same_thread=False)
        self._db_cursor = self._db_connection.cursor()
        logger.debug("Get list of available table names...")
        result_query = self._db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        # creates a table in case if it is absent
        logger.info(f"Creating weather cache '{WEATHER_CACHE_TABLE_NAME}' table ")
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


logger.info(f"Initializing weather db class with '{APP_DB_NAME}' file name.")
weather_db = WeatherCacheDB(APP_DB_NAME)


def get_weather_item_from_db(lat_lon: str, weather_provider_name: str, period: WeatherForecastType) -> Optional[tuple]:
    logger.info(f"Tryint to get weather data with lat-lon: '{lat_lon}', period: '{period.value}' and weather "
                f"provider: '{weather_provider_name}'...")
    try:
        sql_query = f"""SELECT * from {WEATHER_CACHE_TABLE_NAME} WHERE LAT_LON = '{lat_lon}' AND WEATHER_PROVIDER = '{weather_provider_name}' AND PERIOD = '{period.value}'"""
        weather_db.db_cursor.execute(sql_query)
        result = weather_db.db_cursor.fetchone()
    except Exception as err:
        logger.error(f"Failed to get weather data from the DB.\n {err}")
        raise FailedToGetWeatherDataFromDB("Failed to get weather data from the DB.")
    return result


def insert_weather_item_into_db(weather_provider_name: str, timestamp: int, period: WeatherForecastType,
                                weather_data: str, lat_lon: str) -> None:
    logger.info(f"Inserting weather data with lat-lon: '{lat_lon}', period: {period.value} and weather "
                f"provider: '{weather_provider_name}'...")
    try:
        sql_query = f"""INSERT into {WEATHER_CACHE_TABLE_NAME} values (?, ?, ?, ?, ?) """
        weather_db.db_cursor.execute(sql_query, (lat_lon, weather_provider_name, period.value, timestamp, weather_data))
        weather_db.db_connection.commit()
    except Exception as err:
        logger.error(err)
        raise FailedToInsertWeatherDataIntoDB("Failed to insert weather data into the DB.")


def update_weather_item_in_db(weather_provider_name: str, timestamp: int, period: WeatherForecastType,
                              weather_data: str, lat_lon: str) -> None:
    logger.info(f"Updating weather data with lat-lon: '{lat_lon}', period: '{period.value}' and weather "
                f"provider: '{weather_provider_name}'...")
    try:
        sql_query = f""" UPDATE {WEATHER_CACHE_TABLE_NAME} SET TIMESTAMP = {timestamp}, WEATHER_DATA = '{weather_data}' 
        WHERE LAT_LON = '{lat_lon}' AND  WEATHER_PROVIDER = '{weather_provider_name}' AND PERIOD = '{period.value}'"""
        weather_db.db_cursor.execute(sql_query)
        weather_db.db_connection.commit()
    except Exception as err:
        logger.error(err)
        raise FailedToUpdateWeatherDataInDB("Failed to update weather data in the DB.")


def check_weather_cache(weather_provider_name: str, timestamp: int, period: WeatherForecastType, lat_lon: str) -> Tuple[
    bool, Optional[tuple]]:
    """Function checks if combination of location latitude and longitude + weather provider record already exists in DB,
    and it is more than one hour old.
     Returns """
    logger.info(
        f"Checking whether record with lat_lon '{lat_lon}', weather provider '{weather_provider_name}' "
        f"and forecast type '{period.value}' exist in DB.")
    try:
        result = get_weather_item_from_db(lat_lon=lat_lon, weather_provider_name=weather_provider_name, period=period)
    except FailedToCheckWeatherCache:
        err = f"Unable to fetch data for lat-lon: '{lat_lon}' and weather_provider_name: '{weather_provider_name}' " \
              f"from the Weathed Cache DB."
        logger.error(err)
        raise FailedToCheckWeatherCache(err)
    if not result:
        # TODO Raise appropriate exception here
        logger.info(f"Record is not present in the DB.")
        return False, None
    is_cache_actual = check_time_frame(db_timestamp=result[3], current_timestamp=timestamp)
    logger.info(f"Record {result} is actual: {is_cache_actual}")
    return is_cache_actual, result


def update_weather_cache(lat_lon: str, period: WeatherForecastType, weather_provider_name: str, timestamp: int,
                         current_weather_data: str) -> None:
    logger.info("Attempting to update existing weather record in DB...")
    try:
        result = get_weather_item_from_db(lat_lon=lat_lon, weather_provider_name=weather_provider_name, period=period)
        if result:
            if not check_time_frame(db_timestamp=result[3], current_timestamp=timestamp):
                update_weather_item_in_db(weather_provider_name=weather_provider_name, timestamp=timestamp,
                                          weather_data=current_weather_data, lat_lon=lat_lon, period=period)
        else:
            insert_weather_item_into_db(weather_provider_name=weather_provider_name, timestamp=timestamp, period=period,
                                        weather_data=current_weather_data, lat_lon=lat_lon)
    except FailedToCheckWeatherCache as err:
        logger.error(err)
        raise FailedToUpdateWeatherCache("Failed to update weather cache data in the DB.")


def check_time_frame(db_timestamp: Union[int, str], current_timestamp: Union[int, str]) -> bool:
    """Functions checks whether current time exceeds time from DB record for more than an hour."""
    logger.info("Checking if current weather record in DB is exceeded 1 hour time interval...")
    result = not (int(current_timestamp) - int(db_timestamp) > 3600)
    logger.info(f"Timeframe for current weather record is expired: '{result}'")
    return result


if __name__ == '__main__':
    # get_weather_item_from_db()

    # update_weather_item_in_db(lat_lon="46.472500000000025-30.73711000000003", weather_provider_name="Sinoptik",
    #                           timestamp=1652527777,
    #                           weather_data="Some Weather data 4444")
    aaa = get_weather_item_from_db(lat_lon="46.58807000000007-30.941290000000038",
                                   weather_provider_name="Openweathermap", period=WeatherForecastType.CURRENT)
    print(aaa)
