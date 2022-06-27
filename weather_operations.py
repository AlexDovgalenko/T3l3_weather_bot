import logging
from datetime import datetime
from typing import Tuple, Union

from general_symbols import GeneralEmojis
from keyboards.general_keyboards import WeatherForecastType
from weather_cache.weather_cache_exceptions import FailedToCheckWeatherCache, FailedToUpdateWeatherCache
from weather_cache.weather_cache_utils import check_weather_cache, update_weather_cache
from weather_providers.weather_meteomatics import MeteomaticsStrategy
from weather_providers.weather_openweathermap import OpenWeatherMapStrategy
from weather_providers.weather_provider_exception import FailedFetchWeatherDataFromProvider
from weather_providers.weather_provider_strategy import ForecastPeriod, WeatherData, WeatherProviderName

logger = logging.getLogger()

WEATHER_PROVIDER_STRATEGY_DICT = {WeatherProviderName.OPENWEATHERMAP.value: OpenWeatherMapStrategy(),
                                  WeatherProviderName.METEOMATICS.value: MeteomaticsStrategy()}


def return_current_weather_data(weather_provider_name: str, city_name: str,
                                timestamp: int, period: ForecastPeriod, lat_lon: str) -> Tuple[
    Union[WeatherData, str], bool]:
    """Function checks if weather data for provided weather provider, forecast period and coordinates present in the DB."""
    try:
        result, cached_data = check_weather_cache(period=period.CURRENT.value,
                                                  weather_provider_name=weather_provider_name,
                                                  timestamp=timestamp,
                                                  lat_lon=lat_lon)
        if result:
            return cached_data, False
    except FailedToCheckWeatherCache as err:
        logger.error(f"Failed to fetch Weather data from the DB\n{err}")
        raise err
    weather_provider = WEATHER_PROVIDER_STRATEGY_DICT.get(weather_provider_name)
    try:
        return weather_provider.fetch_weather_data(lat_lon=lat_lon, city_name=city_name), True
    except FailedFetchWeatherDataFromProvider:
        logger.error(f"Failed to fetch weather data for city: '{city_name}' and weather provider "
                     f"'{weather_provider_name}'")


def compile_weather_output(lat_lon: str, weather_provider_name: str, forecast_type: WeatherForecastType,
                           city_name: str):
    """Returns HTML pre-formatted weather output for requested location, weather provider and coordinates,
    based on weather forecast type."""
    if forecast_type == WeatherForecastType.CURRENT.value:
        return compile_current_weather_output(weather_provider_name=weather_provider_name, lat_lon=lat_lon,
                                              city_name=city_name)
    elif forecast_type == WeatherForecastType.FIVE_DAYS.value:
        return compile_5d_forecast_weather_output(weather_provider_name=weather_provider_name, lat_lon=lat_lon,
                                                  city_name=city_name)
    else:
        raise RuntimeError(
            f"Unable to compile weather output for the following options:\nWeather provider: {weather_provider_name}"
            f"\nCity name: {city_name}\nLatitude and Longitude: {lat_lon}")


def compile_current_weather_output(weather_provider_name: str, lat_lon: str, city_name: str) -> str:
    """Returns current weather HTML pre-formatted weather output for requested location, weather provider and
    coordinates.

    Function queries weather data for provided weather provider, forecast period and coordinates present in the DB.
    If data exist -- returns data,
    if not -- updated DB with fresh data and returns it.
    In case if it is failed to get weather data - returns text message with corresponding error.
    """
    now = datetime.now()
    date_time_hrs = now.strftime("%Y-%m-%d %H:%M")
    err_msg = f"{GeneralEmojis.POOP.value} Не вдалося отримати данні по населеному пункту **<b> {city_name} **</b>\n" \
              f"Будьласка перевірте назву населеного пункту та повторіть спробу... {GeneralEmojis.POOP.value}"
    text = f"{date_time_hrs}\n==========================\n<code>{err_msg}</code>"
    weather_data, needs_cache_update = return_current_weather_data(weather_provider_name=weather_provider_name,
                                                                   city_name=city_name,
                                                                   timestamp=int(now.timestamp()),
                                                                   period=ForecastPeriod.CURRENT,
                                                                   lat_lon=lat_lon)

    if isinstance(weather_data, tuple):
        text = weather_data[4]

    elif isinstance(weather_data, WeatherData):
        text = f"<b>** {weather_data.city_name} **</b> : \t<b>{date_time_hrs}</b>\n" \
               f"==========================\n" \
               f"<b>Погода</b>:\t{weather_data.weather_emoji}\t{weather_data.weather_summary}\n" \
               f"<b>Температура повітря</b>:\t{weather_data.temperature} С°\n" \
               f"<b>Швидкість вітру</b>:\t{weather_data.wind_speed} м/с\t{weather_data.wind_direction}\n" \
               f"<b>Атмосферний тиск</b>:\t{weather_data.pressure} мм рт.ст.\n" \
               f"<b>Відносна вологість </b>:\t{weather_data.humidity} %\n" \
               f"<b>Схід сонця</b>: {weather_data.sunrise}\n<b>Захід сонця</b>: {weather_data.sunset}"

        try:
            update_weather_cache(lat_lon=weather_data.lat_lon, current_weather_data=text,
                                 period=ForecastPeriod.CURRENT.value,
                                 weather_provider_name=weather_provider_name,
                                 timestamp=int(weather_data.timestamp))
        except FailedToUpdateWeatherCache as err:
            logger.error(err)
    return text


def compile_5d_forecast_weather_output(weather_provider_name: str, lat_lon: str, city_name: str) -> str:
    raise NotImplementedError("This option is in development phase...")
