from typing import TYPE_CHECKING

from aiogram import types
from aiogram.types import InlineKeyboardButton

from general_symbols import SpecialSymbols, GeneralEmojis
from weather_providers.weather_provider_strategy import WeatherProviderName

if TYPE_CHECKING:
    from aiogram.types import InlineKeyboardMarkup


def reply_languages_keyboard() -> "InlineKeyboardMarkup":
    """Returns keyboard containing available language options
    :return: InlineKeyboardMarkup --> Inline keyboard containing available language options
    """
    ua_flags_button = InlineKeyboardButton(text=GeneralEmojis.UA_FLAG.value, callback_data=GeneralEmojis.UA_FLAG.value)
    us_flags_button = InlineKeyboardButton(text=GeneralEmojis.US_FLAG.value, callback_data=GeneralEmojis.US_FLAG.value)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.add(ua_flags_button, us_flags_button)
    return keyboard


def reply_weather_provider_keyboard() -> "InlineKeyboardMarkup":
    """Represents list of available weather providers.
    :return: InlineKeyboardMarkup --> Inline keyboard containing available weather providers
    """
    weather_providers_buttons_text = [wp.value for wp in WeatherProviderName]
    weather_providers_buttons = [InlineKeyboardButton(
        text=f"{SpecialSymbols.ARROW_UP.value} {text} {SpecialSymbols.ARROW_UP.value}", callback_data=text) for text in
        weather_providers_buttons_text]
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*weather_providers_buttons)
    return keyboard
