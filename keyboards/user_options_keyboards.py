from aiogram import types
from aiogram.types import InlineKeyboardButton

from keyboards.common_emoji_codes import ua_flag_emoji, us_flag_emoji, crossed_flags_emoji, weather_forecast_emoji
from weather_providers.weather_provider_strategy import WeatherProviderName

weather_providers_names_list = [wp.value for wp in WeatherProviderName]


def reply_languages_keyboard():
    ua_flags_button = InlineKeyboardButton(text=ua_flag_emoji, callback_data=ua_flag_emoji)
    us_flags_button = InlineKeyboardButton(text=us_flag_emoji, callback_data=us_flag_emoji)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.add(ua_flags_button, us_flags_button)
    return keyboard


def reply_weather_provider_keyboard():
    weather_providers_buttons_text = [wp.value for wp in WeatherProviderName]
    weather_providers_buttons = [InlineKeyboardButton(text=text, callback_data=text) for text in weather_providers_buttons_text]
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*weather_providers_buttons)
    return keyboard


def reply_options_config_keyboard():
    options_config_button = [crossed_flags_emoji, "weather provider"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*options_config_button)
    return keyboard


# def reply_languages_keyboard():
#     # flags_button = [ua_flag_emoji, us_flag_emoji]
#     flags_button = ["ua_flag_emoji", "us_flag_emoji"]
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     keyboard.add(*flags_button)
#     return keyboard
#
#
# def reply_weather_provider_keyboard():
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     keyboard.add(*weather_providers_names_list)
#     return keyboard
