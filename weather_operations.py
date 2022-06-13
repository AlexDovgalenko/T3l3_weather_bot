import logging
from datetime import datetime
from typing import Tuple, Union

from keyboards.common_emoji_codes import poop_emoji
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
                                timestamp: int, period: ForecastPeriod) -> Tuple[Union[WeatherData, str], bool]:
    try:
        result, cached_data = check_weather_cache(city_name=city_name,
                                                  period=period.CURRENT.value,
                                                  weather_provider_name=weather_provider_name,
                                                  timestamp=timestamp)
        if result:
            return cached_data, False
    except FailedToCheckWeatherCache as err:
        logger.error(f"Failed to fetch Weather data from the DB\n{err}")
        raise err
    weather_provider = WEATHER_PROVIDER_STRATEGY_DICT.get(weather_provider_name)
    try:
        return weather_provider.fetch_weather_data(city_name=city_name), True
    except FailedFetchWeatherDataFromProvider:
        logger.error(f"Failed to fetch weather data for city: '{city_name}' and weather provider "
                     f"'{weather_provider_name}'")


def compile_current_weather_output(weather_provider_name: str, city_name: str) -> str:
    now = datetime.now()
    date_time_hrs = now.strftime("%Y-%m-%d %H:%M")
    err_msg = f"{poop_emoji} Не вдалося отримати данні по населеному пункту **<b> {city_name} **</b>\n" \
              f"Будьласка перевірте назву населеного пункту та повторіть спробу... {poop_emoji}"
    text = f"{date_time_hrs}\n==========================\n<code>{err_msg}</code>"
    weather_data, needs_cache_update = return_current_weather_data(weather_provider_name=weather_provider_name,
                                                                   city_name=city_name,
                                                                   timestamp=int(now.timestamp()),
                                                                   period=ForecastPeriod.CURRENT)

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
