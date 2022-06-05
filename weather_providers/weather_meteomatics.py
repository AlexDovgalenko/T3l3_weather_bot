"""Module contains data to work with meteomatics.com weather API resource."""

import logging
import os
from datetime import datetime
from pprint import pprint
from typing import Optional, Union

import requests
from dotenv import load_dotenv

from geocoding.geocoding_utils import get_lat_lon_from_city_name
from weather_providers.weather_provider_strategy import WeatherProviderStrategy, WeatherData, ForecastPeriod, \
    WeatherProviderName

load_dotenv()

logger = logging.getLogger()

METEOMATICS_USERNAME = os.environ.get("METEOMATICS_USERNAME")
METEOMATICS_PASSWORD = os.environ.get("METEOMATICS_PASSWORD")

parameters = "wind_speed_10m:ms,wind_dir_10m:d,t_2m:C,msl_pressure:hPa,weather_symbol_1h:idx,precip_24h:mm,t_max_2m_24h:C,t_min_2m_24h:C"


class MeteomaticsStrategy(WeatherProviderStrategy):
    provider_name = WeatherProviderName.METEOMATICS
    base_url = "api.meteomatics.com"

    def _get_weather_response(self, city_name: str) -> Optional[dict]:
        location = ",".join(get_lat_lon_from_city_name(city_name))
        current_datetime = f"{datetime.now().strftime('%Y-%m-%dT%H:%M')}+02:00"
        if not location:
            logger.error(f"Unable to get latitude and longitude tor given city name: {city_name}")
            return None
        try:
            response = requests.get(
                f"http://{METEOMATICS_USERNAME}:{METEOMATICS_PASSWORD}@{self.base_url}/"
                f"{current_datetime}/{parameters}/{location}/json")
        except Exception as exception:
            logger.error(exception)
            return None
        return response.json()

    def fetch_weather_data(self, city_name: str, period_option: ForecastPeriod = ForecastPeriod.CURRENT) -> Union[
        WeatherData, str]:
        pass

    def _parse_current_weather(self, city_name, weather_response: dict):
        pass

    def _parse_weather_forecast(self, city_name, weather_response: dict):
        pass


if __name__ == '__main__':
    pass
