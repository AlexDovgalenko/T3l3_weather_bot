from aiogram import types
from aiogram.types import InlineKeyboardButton


def weather_forecast_type():
    current_forecast = InlineKeyboardButton(text="Поточна погода", callback_data="_forecast_weather_current")
    five_days_forecast = InlineKeyboardButton(text="Прогноз на 5 днів", callback_data="_forecast_weather_five_days")
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.add(current_forecast, five_days_forecast)
    return keyboard
