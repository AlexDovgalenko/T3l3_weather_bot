from abc import abstractmethod, ABC
from typing import Optional, Union

from main import WeatherData
from weather_providers.weather_openweathermap import ForecastPeriod


class WeatherProviderStrategy(ABC):

    provider_name: str

    @abstractmethod
    def __get_weather_response(self, city_name: str) -> Optional[dict]:
        """ Method gets weather response from sertain weather API resource

        :param city_name: Name of the city to find out weather
        :return:
        """

    @abstractmethod
    def get_weather_data(self, city_name: str, period_option: Optional[ForecastPeriod] = ForecastPeriod.CURRENT) -> Union[
            "WeatherData", str]:
        pass

    @abstractmethod
    def __parse_current_weather(self, city_name, weather_response: dict):
        pass

    @abstractmethod
    def __parse_weather_forecast(self, city_name, weather_response: dict):
        pass
