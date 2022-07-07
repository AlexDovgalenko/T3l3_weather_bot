from typing import TYPE_CHECKING, List

from aiogram import types
from aiogram.types import InlineKeyboardButton

from geocoding.geocoding_utils import LocationPoint
from weather_providers.weather_provider_strategy import WeatherForecastType

if TYPE_CHECKING:
    from aiogram.types import InlineKeyboardMarkup


def weather_forecast_type_keyboard() -> "InlineKeyboardMarkup":
    """Represents keyboard with available weather output options

    Currently, only 3 options available: 'current weather', 'today's weather' and '5 days forecast'
    :return: InlineKeyboardMarkup --> Inline keyboard containing possible forecast options
    """
    current_forecast = InlineKeyboardButton(text="Зараз",
                                            callback_data=WeatherForecastType.CURRENT.value)
    today_forecast = InlineKeyboardButton(text="На день",
                                              callback_data=WeatherForecastType.TODAY.value)
    five_days_forecast = InlineKeyboardButton(text="На 5 днів",
                                              callback_data=WeatherForecastType.FIVE_DAYS.value)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.add(current_forecast, today_forecast, five_days_forecast)
    return keyboard


def city_specification_items_keyboard(available_location_options: List[LocationPoint]) -> "InlineKeyboardMarkup":
    """Represents list of available location options by provided city name.
    :param available_location_options: provided available list of locations options
    :return: InlineKeyboardMarkup --> Inline keyboard containing all possible location options
    """
    location_options_buttons = [InlineKeyboardButton(text=location.address, callback_data=location.lat_lon) for
                                location in available_location_options]
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*location_options_buttons)
    return keyboard
