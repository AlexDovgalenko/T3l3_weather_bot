import json
import logging
import os
from datetime import datetime
from enum import Enum
from pprint import pprint
from typing import Optional, Union

import requests
from dotenv import load_dotenv

from geocoding import get_lat_lon_from_city_name
from main import WeatherData
from utils import hpa_to_mm_hg_converter, math_round
from weather_emoji import get_weather_emojy, WeatherProvider

load_dotenv()

OPEN_WEATHER_API_KEY = os.environ.get("OPEN_WEATHER_API_KEY")
COUNTRY_NAME = os.environ.get("COUNTRY_NAME")

UNITS = "metric"
LANGUAGE = "US"

logger = logging.getLogger()


class Language(Enum):
    UA: int = 1
    US: int = 2


class ForecastPeriod(Enum):
    """Class stores period option for query weather"""
    CURRENT: int = 1
    FORECAST: int = 2


def get_weather_response(city_name: str) -> Optional[dict]:
    """ Method gets weather response from api.openweathermap.org

    :param city_name: Name of the city to find out weather
    :return:
    """
    latitude, longitude = get_lat_lon_from_city_name(city_name)

    if not (latitude or longitude):
        logger.error(f"Unable to get latitude and longitude tor given city name: {city_name}")
        return None
    try:
        response = requests.get(
            # f"https://api.openweathermap.org/data/2.5/{period_option.value}?lat={latitude}&lon={longitude}&appid={OPEN_WEATHER_API_KEY}&lang={LANGUAGE}&units={UNITS}&mode=json").json()
            f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&appid={OPEN_WEATHER_API_KEY}&lang={LANGUAGE}&exclude=hourly,minutely,alerts&units={UNITS}&mode=json")
    except Exception as exception:
        logger.error(exception)
        return None
    if response.status_code != 200:
        logger.error(f"Response code is not equals to 200: <{response.status_code}>\n{response.reason}")
        return None
    return json.loads(response.text)


def get_weather_data(city_name: str, period_option: ForecastPeriod = ForecastPeriod.CURRENT) -> Union[WeatherData, str]:
    response = get_weather_response(city_name)
    err_msg = f"Не вдалося отримати данні по населеному пункту **<b> {city_name} **</b>\n" \
              f"Будьласка перевірте чи правильно ви ввели назву населеного пункту та повторіть спробу..."

    if not response:
        return err_msg

    else:
        if period_option is ForecastPeriod.CURRENT:
            weather_data = parse_current_weather(city_name, weather_response=response)
        elif ForecastPeriod.FORECAST:
            weather_data = parse_weather_forecast(city_name, weather_response=response)
        else:
            logger.error(f"Incorrect 'period_option' waw passed, possible options are:{list(ForecastPeriod)}")
            return err_msg
    if not weather_data:
        return err_msg
    return weather_data


def parse_current_weather(city_name, weather_response: dict):
    try:
        emoji_data = get_weather_emojy(
            weather_provider=WeatherProvider.OPENWEATHERMAP,
            weather_code=weather_response["current"]["weather"][0].get("id")
        )
        weather_data = WeatherData(
            city_name=city_name,
            date=datetime.now().strftime("%Y-%m-%d"),
            weather_emoji=emoji_data[0],
            weather_summary=emoji_data[1],
            temperature=math_round(weather_response["current"].get("temp")),
            max_temperature=math_round(weather_response["current"].get("temp_max")) if weather_response["current"].get(
                "temp_max") else None,
            min_temperature=math_round(weather_response["current"].get("temp_min")) if weather_response["current"].get(
                "temp_min") else None,
            wind_speed=weather_response["current"].get("wind_speed"),
            wind_direction=weather_response["current"].get("wind_deg"),
            pressure=hpa_to_mm_hg_converter(weather_response["current"].get("pressure")),
            precipitation=weather_response["current"].get("precipitation"),
            humidity=weather_response["current"].get("humidity"),
            sunrise=weather_response["current"].get("sunrise"),
            sunset=weather_response["current"].get("sunset"))
    except Exception as err:
        logger.error(f"Failed to parse weather response because of following error:\n{err}")
        return None
    return weather_data


def parse_weather_forecast(city_name, weather_response: dict):
    try:
        emoji_data = get_weather_emojy(
            weather_provider=WeatherProvider.OPENWEATHERMAP,
            weather_code=weather_response["current"]["weather"][0].get("id")
        )
        weather_data_list = []
        for item in range(1, 6):
            weather_data = WeatherData(
                city_name=city_name,
                date=weather_response['daily'][item].get("dt"),
                weather_emoji=emoji_data[0],
                weather_summary=emoji_data[1],
                max_temperature=math_round(weather_response['daily'][item]["temp"].get("max")),
                min_temperature=math_round(weather_response['daily'][item]["temp"].get("min")),
                temperature=math_round(weather_response['daily'][item]["temp"].get("temp")) if
                weather_response['daily'][item]["temp"].get("temp") else None,
                wind_speed=weather_response['daily'][item].get("wind_speed"),
                wind_direction=weather_response['daily'][item].get("wind_deg"),
                pressure=hpa_to_mm_hg_converter(weather_response['daily'][item].get("pressure")),
                precipitation=weather_response['daily'][item].get("precipitation"),
                humidity=weather_response['daily'][item].get("humidity"),
                sunrise=weather_response['daily'][item].get("sunrise"),
                sunset=weather_response['daily'][item].get("sunset"))

            weather_data_list.append(weather_data)
    except Exception as err:
        logger.error(f"Failed to parse weather response because of following error:\n{err}")
        return None
    return weather_data_list


if __name__ == '__main__':
    # pprint(get_weather_response("Odesa"))
    pprint(get_weather_data("Kyiv"))
