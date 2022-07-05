from datetime import datetime
from typing import Tuple, Union, List
from loguru import logger
from weather_cache.weather_cache_exceptions import FailedToCheckWeatherCache, FailedToUpdateWeatherCache
from weather_cache.weather_cache_utils import check_weather_cache, update_weather_cache
from weather_providers.weather_meteomatics import MeteomaticsStrategy
from weather_providers.weather_openweathermap import OpenWeatherMapStrategy
from weather_providers.weather_provider_exception import FailedFetchWeatherDataFromProvider
from weather_providers.weather_provider_strategy import WeatherData, WeatherProviderName, WeatherForecastType

WEATHER_PROVIDER_STRATEGY_DICT = {WeatherProviderName.OPENWEATHERMAP.value: OpenWeatherMapStrategy(),
                                  WeatherProviderName.METEOMATICS.value: MeteomaticsStrategy()}

WEATHER_DODY_TEMPLATE_DICT = {
    "date": "<b>Погода на:</b> \t<date>\n==================================",
    "weather_emoji": "<b>Погода</b>:\t<weather_emoji>\t<weather_summary>",
    "max_temperature": "<b>Максимальна температура повітря</b>:\t<max_temperature> С°",
    "min_temperature": "<b>Мінімальна температура повітря</b>:\t<min_temperature> С°",
    "wind_speed": "<b>Швидкість вітру</b>:\t<wind_speed> м/с\t<wind_direction>",
    "pressure": "<b>Атмосферний тиск</b>:\t<pressure> мм рт.ст.",
    "precipitation": "<b>Опади</b>:\t<precipitation> мм",
    "humidity": "<b>Відносна вологість </b>:\t<humidity> %",
    "sunrise": "<b>Схід сонця</b>: <sunrise>",
    "sunset": "<b>Захід сонця</b>: <sunset>",
}


def compile_weather_output(lat_lon: str, weather_provider_name: str, forecast_type: str, city_name: str) -> str:
    """Returns HTML pre-formatted weather output for requested location, weather provider and coordinates,
    based on weather forecast type."""
    period = WeatherForecastType(forecast_type)
    try:
        compilled_weather_output = __get_and_update_weather(weather_provider_name=weather_provider_name,
                                                            lat_lon=lat_lon,
                                                            city_name=city_name, period=period)
        return compilled_weather_output
    except Exception:
        raise RuntimeError(
            f"Unable to compile weather output for the following options:\nWeather provider: {weather_provider_name}"
            f"\nCity name: {city_name}\nLatitude and Longitude: {lat_lon}")


def __get_and_update_weather(weather_provider_name: str, lat_lon: str, city_name: str,
                             period: WeatherForecastType) -> str:
    """Returns current weather HTML pre-formatted weather output for requested location, weather provider and
    coordinates.

    Function queries weather data for provided weather provider, forecast period and coordinates present in the DB.
    If data exist -- returns data,
    if not -- updated DB with fresh data and returns it.
    In case if it is failed to get weather data - returns text message with corresponding error.
    """
    now = datetime.now()
    weather_data, needs_cache_update = __return_weather_data(weather_provider_name=weather_provider_name,
                                                             city_name=city_name,
                                                             timestamp=int(now.timestamp()),
                                                             period=period,
                                                             lat_lon=lat_lon)

    if isinstance(weather_data, tuple):
        text = weather_data[4]
        return text

    elif isinstance(weather_data, (WeatherData, list)):
        text = __compile_weather_string(weather_data, period=period)
        try:
            update_weather_cache(
                lat_lon=weather_data[0].lat_lon if isinstance(weather_data, list) else weather_data.lat_lon,
                current_weather_data=text,
                period=period,
                weather_provider_name=weather_provider_name,
                timestamp=int(weather_data[0].timestamp)) if isinstance(weather_data, list) else int(
                weather_data.timestamp)
        except FailedToUpdateWeatherCache as err:
            logger.error(err)
        return text


def __return_weather_data(weather_provider_name: str, city_name: str, timestamp: int, period: WeatherForecastType,
                          lat_lon: str) -> Tuple[Union[WeatherData, tuple], bool]:
    """Function checks if weather data for provided weather provider, forecast period and coordinates present in the DB,
     if Yes, returns existing cached data, else, fetches weather data from weather provider.

     :param weather_provider_name: string with weather provider name
     :param city_name: string with location to get weather
     :param timestamp: current timestamp
     :param period: instance of WeatherForecastType class
     :param lat_lon: string containing latitude and longitude in "46.58807000000007-30.941290000000038" format
     :return: Tuple[Union[WeatherData, tuple] -- cached or freshly fetched weather data from weather provider,
     bool -- indicator whether it requres to updated weather cache]
     """
    logger.info("Checking weather cache ...")
    try:
        is_cached_data_actual, cached_data = check_weather_cache(period=period,
                                                                 weather_provider_name=weather_provider_name,
                                                                 timestamp=timestamp,
                                                                 lat_lon=lat_lon)
        if is_cached_data_actual:
            return cached_data, False
    except FailedToCheckWeatherCache as err:
        logger.error(f"Failed to fetch Weather data from the DB\n{err}")
        raise err
    weather_provider = WEATHER_PROVIDER_STRATEGY_DICT.get(weather_provider_name)
    try:
        weather_data = weather_provider.fetch_weather_data(lat_lon=lat_lon, city_name=city_name, period=period)
        if not weather_data:
            raise FailedFetchWeatherDataFromProvider
        return weather_data, True
    except FailedFetchWeatherDataFromProvider:
        logger.error(f"Failed to fetch weather data for city: '{city_name}' and weather provider "
                     f"'{weather_provider_name}'")


def __build_weather_string_list(weather_data: WeatherData):
    weather_body_list = [v for k, v in
                         WEATHER_DODY_TEMPLATE_DICT.items() if weather_data.__getattribute__(k)]
    return weather_body_list


def __compile_weather_string(weather_data: Union[WeatherData, List[WeatherData]], period: WeatherForecastType):
    if isinstance(weather_data, WeatherData):
        weather_header_template = "<b>** <city_name> **</b>\n".replace("<city_name>", str(weather_data.city_name))
        weather_body_list = __build_weather_string_list(weather_data=weather_data)
        weather_body_string = "\n".join(weather_body_list)
        for key, value in weather_data.__dict__.items():
            if key in weather_body_string:
                if key == "date" and period == WeatherForecastType.CURRENT:
                    weather_body_string = weather_body_string.replace(f"<{key}>",
                                                                      str(datetime.now().strftime("%Y-%m-%d %H:%M")))
                weather_body_string = weather_body_string.replace(f"<{key}>", str(value))
        final_weather_string = "\n".join((weather_header_template, weather_body_string))
        return f"{final_weather_string}\n=================================="

    if isinstance(weather_data, list):
        weather_header_template = "<b>** <city_name> **</b>\n".replace("<city_name>", str(weather_data[0].city_name))
        weather_body_string = __build_string_body_from_list(weather_data=weather_data)
        final_weather_string = "\n".join((weather_header_template, weather_body_string))
        return final_weather_string


def __build_string_body_from_list(weather_data: List[WeatherData]) -> str:
    final_string = ""
    for item in weather_data:
        weather_body_list = __build_weather_string_list(weather_data=item)
        weather_body_string = "\n".join(weather_body_list)
        for key, value in item.__dict__.items():
            if key in weather_body_string:
                weather_body_string = weather_body_string.replace(f"<{key}>", str(value))
        final_string += f"{weather_body_string}\n==================================\n\n"
    return final_string
