"""Contains custom exceptions related to "weather_cache_utils.py" module"""


class FailedFetchWeatherDataFromProvider(Exception):
    """General exception raised from Weather Providers module if it failed to fetch weather data."""
