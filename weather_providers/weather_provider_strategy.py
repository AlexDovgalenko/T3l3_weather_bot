from abc import abstractmethod, ABC
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union


class WeatherProviderName(Enum):
    OPENWEATHERMAP = "Openweathermap"
    METEOMATICS = "Meteomatics"
    SINOPTIC = "Sinoptik"


class WeatherForecastType(Enum):
    CURRENT = "_forecast_weather_current"
    FIVE_DAYS = "_forecast_weather_five_days"


@dataclass
class WeatherData:
    city_name: str
    lat_lon: Optional[str]
    timestamp: str
    date: str
    weather_emoji: str
    weather_summary: str
    temperature: Optional[str]
    max_temperature: Optional[str]
    min_temperature: Optional[str]
    wind_speed: str
    wind_direction: Optional[str]
    pressure: str
    precipitation: Optional[str]
    humidity: Optional[str]
    sunrise: Optional[str]
    sunset: Optional[str]


class WeatherProviderStrategy(ABC):
    provider_name: WeatherProviderName
    base_url: str

    @abstractmethod
    def _get_weather_response(self, city_name: str) -> Optional[dict]:
        """ Method gets weather response from sertain weather API resource

        :param city_name: Name of the city to find out weather
        :return:
        """

    @abstractmethod
    def fetch_weather_data(self, lat_lon: str, city_name: str,
                           period_option: "WeatherForecastType" = WeatherForecastType.CURRENT) -> \
            Union["WeatherData", str]:
        pass

    @abstractmethod
    def _parse_current_weather(self, city_name, weather_response: dict):
        pass

    @abstractmethod
    def _parse_weather_forecast(self, city_name, weather_response: dict):
        pass
