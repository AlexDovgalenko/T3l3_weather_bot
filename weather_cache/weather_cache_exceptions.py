"""Contains custom exceptions related to "weather_cache_utils.py" module"""


class FailedToCheckWeatherCache(Exception):
    """General error raised from Weather Cache module"""


class FailedToInsertWeatherDataIntoDB(FailedToCheckWeatherCache):
    """Exception raised in case if it is failed to insert weather data into DB."""


class FailedToGetWeatherDataFromDB(FailedToCheckWeatherCache):
    """Exception raised in case if it if failed to read weather data from DB."""


class FailedToUpdateWeatherDataInDB(FailedToCheckWeatherCache):
    """Exception raised in case if it is failed to update weather data within the DB."""


class FailedToUpdateWeatherCache(Exception):
    """Exception raised from Weather Cache module if it was failed to update weather data cache"""
