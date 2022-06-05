import logging
import os
from datetime import datetime

import telegram.ext.filters
from dotenv import load_dotenv, find_dotenv
from telegram import Update, ParseMode
from telegram.ext import CommandHandler, Updater, CallbackQueryHandler, CallbackContext, MessageHandler

from wather_cache.weather_cache_utils import check_weather_cache
from weather_providers.weather_openweathermap import OpenWeatherMapStrategy
from weather_providers.weather_provider_strategy import WeatherProviderStrategy, WeatherData

load_dotenv(find_dotenv())
logger = logging.getLogger()

BOT_HASH = os.environ.get("BOT_HASH")

WEATHER_PROVIDER = OpenWeatherMapStrategy()


def return_current_weather_data(weather_provider: WeatherProviderStrategy, city_name: str,
                                date_time: datetime) -> WeatherData:
    result, cached_data = check_weather_cache(city_name=city_name,
                                              weather_provider_name=WeatherProviderStrategy.provider_name.value,
                                              timestamp=int(date_time.timestamp()))
    if result:
        return cached_data
    return weather_provider.get_weather_data(city_name=city_name)


def compile_current_weather_output(weather_provider: WeatherProviderStrategy, city_name: str) -> str:
    now = datetime.now()
    date_time_hrs = now.strftime("%Y-%m-%d %H:%M")
    weather_data = return_current_weather_data(weather_provider=weather_provider, city_name=city_name, date_time=now)
    if isinstance(weather_data, WeatherData):
        text = f"<b>** {weather_data.city_name} **</b> : \t<b>{date_time_hrs}</b>\n" \
               f"==========================\n" \
               f"<b>Погода</b>:\t{weather_data.weather_emoji}\t{weather_data.weather_summary}\n" \
               f"<b>Температура повітря</b>:\t{weather_data.temperature} С°\n" \
               f"<b>Швидкість вітру</b>:\t{weather_data.wind_speed} м/с\t{weather_data.wind_direction}\n" \
               f"<b>Атмосферний тиск</b>:\t{weather_data.pressure} мм рт.ст.\n" \
               f"<b>Відносна вологість </b>:\t{weather_data.humidity} %\n" \
               f"<b>Схід сонця</b>: {weather_data.sunrise}\n<b>Захід сонця</b>: {weather_data.sunset}"

    else:
        text = f"{date_time_hrs}\n==========================\n<code>{weather_data}</code>"
    return text


def reply_current_weather_result(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    weather_text = compile_current_weather_output(city_name=update.message.text, weather_provider=WEATHER_PROVIDER)
    # keyboard = [[KeyboardButton(text="Оберіть назву населеного пункту...")]]
    # reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True,)
    # reply_markup = InlineKeyboardMarkup(keyboard)=
    context.bot.send_message(text=weather_text, chat_id=chat_id, parse_mode=ParseMode.HTML)


def start(update: Update, _: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    # keyboard = [[KeyboardButton(text="Оберіть назву населеного пункту...")]]
    # reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True, )
    # update.message.reply_text(te, reply_markup=reply_markup)
    chat_id = update.message.chat_id
    update.message.bot.send_message(chat_id=chat_id, text="<b>Оберіть назву населеного пункту...</b>",
                                    parse_mode=ParseMode.HTML)


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    query.answer()
    reply_current_weather_result(query, context)


def bot_main():
    updater = Updater(BOT_HASH)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(filters=telegram.ext.filters.Filters.text, callback=reply_current_weather_result))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    bot_main()
