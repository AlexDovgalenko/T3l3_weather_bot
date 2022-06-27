from enum import Enum
from typing import TYPE_CHECKING, List

from aiogram import types
from aiogram.types import InlineKeyboardButton
from geocoding.geocoding_utils import LocationPoint

if TYPE_CHECKING:
    from aiogram.types import InlineKeyboardMarkup


class WeatherForecastType(Enum):
    CURRENT = "_forecast_weather_current"
    FIVE_DAYS = "_forecast_weather_five_days"


def weather_forecast_type_keyboard() -> "InlineKeyboardMarkup":
    """Represents keyboard with available weather output options

    Currently, only 2 options available: 'current weather' and '5 days forecast'
    :return: InlineKeyboardMarkup --> Inline keyboard containing possible forecast options
    """
    current_forecast = InlineKeyboardButton(text="Поточна погода",
                                            callback_data=WeatherForecastType.CURRENT.value)
    five_days_forecast = InlineKeyboardButton(text="Прогноз на 5 днів",
                                              callback_data=WeatherForecastType.FIVE_DAYS.value)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.add(current_forecast, five_days_forecast)
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
