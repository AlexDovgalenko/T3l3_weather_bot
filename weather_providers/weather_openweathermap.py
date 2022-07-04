import json
from datetime import datetime
from enum import Enum
from typing import Optional, List, Tuple

import requests
from loguru import logger

from config import OPEN_WEATHER_API_KEY
from geocoding.geocoding_utils import get_lat_lon_from_attribute
from utils import hpa_to_mm_hg_converter, math_round
from weather_emoji import get_weather_emojy
from weather_providers.weather_provider_strategy import WeatherData, WeatherProviderStrategy, WeatherForecastType, \
    WeatherProviderName
from wind_direction_emoji import get_wind_direction_emoji

UNITS = "metric"
LANGUAGE = "US"


class Language(Enum):
    UA: int = 1
    US: int = 2


class OpenWeatherMapStrategy(WeatherProviderStrategy):
    provider_name = WeatherProviderName.OPENWEATHERMAP.value
    base_url = "api.openweathermap.org"

    def _get_weather_response(self, lat_lon: str) -> Optional[Tuple[dict, str]]:
        """ Method gets weather response from api.openweathermap.org

        :param lat_lon: latitude and longitude for chosen geolocation
        :return:
        """
        latitude, longitude = get_lat_lon_from_attribute(lat_lon)
        try:
            response = requests.get(
                # f"https://api.openweathermap.org/data/2.5/{period_option.value}?lat={latitude}&lon={longitude}&appid={OPEN_WEATHER_API_KEY}&lang={LANGUAGE}&units={UNITS}&mode=json").json()
                f"https://{self.base_url}/data/2.5/onecall?lat={latitude}&lon={longitude}&appid={OPEN_WEATHER_API_KEY}&lang={LANGUAGE}&exclude=hourly,minutely,alerts&units={UNITS}&mode=json")
        except Exception as exception:
            logger.error(exception)
            return None
        if response.status_code != 200:
            logger.error(f"Response code is not equals to 200: <{response.status_code}>\n{response.reason}")
            return None
        return json.loads(response.text), "-".join([latitude, longitude])

    def fetch_weather_data(self, lat_lon: str, city_name: str, period: WeatherForecastType) -> Optional[WeatherData]:

        response = self._get_weather_response(lat_lon=lat_lon)

        if not response:
            return None
        else:
            if period is WeatherForecastType.CURRENT:
                weather_data = self._parse_current_weather(city_name, weather_response=response)
            elif period in [WeatherForecastType.FIVE_DAYS]:
                weather_data = self._parse_weather_forecast(city_name, weather_response=response)
            else:
                logger.error(f"Incorrect 'period_option' waw passed, possible options are:{list(WeatherForecastType)}")
                return None
        if not weather_data:
            return None
        return weather_data

    def _parse_current_weather(self, city_name, weather_response: Tuple[dict, str]) -> Optional[WeatherData]:
        try:
            emoji_data = get_weather_emojy(
                weather_provider_name=self.provider_name,
                weather_code=weather_response[0]["current"]["weather"][0].get("id")
            )
            weather_data = WeatherData(
                city_name=city_name,
                lat_lon=weather_response[1],
                timestamp=weather_response[0]["current"].get("dt"),
                date=datetime.now().strftime("%Y-%m-%d"),
                weather_emoji=emoji_data[0],
                weather_summary=emoji_data[1],
                temperature=math_round(weather_response[0]["current"].get("temp")),
                max_temperature=math_round(weather_response[0]["current"].get("temp_max")) if weather_response[0][
                    "current"].get(
                    "temp_max") else None,
                min_temperature=math_round(weather_response[0]["current"].get("temp_min")) if weather_response[0][
                    "current"].get(
                    "temp_min") else None,
                wind_speed=weather_response[0]["current"].get("wind_speed"),
                wind_direction=get_wind_direction_emoji(weather_response[0]["current"].get("wind_deg")),
                pressure=hpa_to_mm_hg_converter(weather_response[0]["current"].get("pressure")),
                precipitation=weather_response[0]["current"].get("precipitation"),
                humidity=weather_response[0]["current"].get("humidity"),
                sunrise=datetime.fromtimestamp(weather_response[0]["current"].get("sunrise")).strftime(
                    "%Y-%m-%d %H:%M:%S"),
                sunset=datetime.fromtimestamp(weather_response[0]["current"].get("sunset")).strftime(
                    "%Y-%m-%d %H:%M:%S")
            )
        except Exception as err:
            logger.error(f"Failed to parse weather response because of following error:\n{err}")
            return None
        return weather_data

    def _parse_weather_forecast(self, city_name, weather_response: Tuple[dict, str]) -> Optional[List[WeatherData]]:
        try:
            emoji_data = get_weather_emojy(
                weather_provider_name=self.provider_name,
                weather_code=weather_response[0]["current"]["weather"][0].get("id")
            )
            weather_data_list = []
            for item in range(6):
                weather_data = WeatherData(
                    city_name=city_name,
                    lat_lon=weather_response[1],
                    timestamp=weather_response[0]['daily'][item].get("dt"),
                    date=datetime.fromtimestamp(weather_response[0]['daily'][item].get("dt")).strftime("%Y-%m-%d"),
                    weather_emoji=emoji_data[0],
                    weather_summary=emoji_data[1],
                    max_temperature=math_round(weather_response[0]['daily'][item]["temp"].get("max")),
                    min_temperature=math_round(weather_response[0]['daily'][item]["temp"].get("min")),
                    temperature=math_round(weather_response[0]['daily'][item]["temp"].get("temp")) if
                    weather_response[0]['daily'][item]["temp"].get("temp") else None,
                    wind_speed=weather_response[0]['daily'][item].get("wind_speed"),
                    wind_direction=get_wind_direction_emoji(weather_response[0]['daily'][item].get("wind_deg")),
                    pressure=hpa_to_mm_hg_converter(weather_response[0]['daily'][item].get("pressure")),
                    precipitation=weather_response[0]['daily'][item].get("precipitation"),
                    humidity=weather_response[0]['daily'][item].get("humidity"),
                    sunrise=datetime.fromtimestamp(weather_response[0]['daily'][item].get("sunrise")).strftime(
                        "%Y-%m-%d %H:%M:%S"),
                    sunset=datetime.fromtimestamp(weather_response[0]['daily'][item].get("sunset")).strftime(
                        "%Y-%m-%d %H:%M:%S")
                )

                weather_data_list.append(weather_data)
        except Exception as err:
            logger.error(f"Failed to parse weather response because of following error:\n{err}")
            return None
        return weather_data_list
