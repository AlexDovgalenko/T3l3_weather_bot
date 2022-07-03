import logging

from config import BOT_HASH
from weather_providers.weather_openweathermap import OpenWeatherMapStrategy
from loguru import logger
# logger = logging.getLogger()

WEATHER_PROVIDER = OpenWeatherMapStrategy()


# def reply_current_weather_result(update: Update, context: CallbackContext):
#     chat_id = update.message.chat_id
#     message_id = update.message.message_id
#     weather_text = compile_current_weather_output(city_name=update.message.text, weather_provider=WEATHER_PROVIDER)
#     # keyboard = [[KeyboardButton(text="Оберіть назву населеного пункту...")]]
#     # reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True,)
#     # reply_markup = InlineKeyboardMarkup(keyboard)=
#     context.bot.send_message(text=weather_text, chat_id=chat_id, parse_mode=ParseMode.HTML)


def start(update: Update, _: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    # keyboard = [[KeyboardButton(text="Оберіть назву населеного пункту...")]]
    # reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True, )
    # update.message.reply_text(te, reply_markup=reply_markup)
    chat_id = update.message.chat_id
    update.message.bot.send_message(chat_id=chat_id, text="<b>Оберіть назву населеного пункту...</b>",
                                    parse_mode=ParseMode.HTML)


def user_options(update: Update, _: CallbackContext) -> None:
    chat_id = update.message.chat_id
    keyboard = [[KeyboardButton(text="Оберіть назву населеного пункту...")]]
    reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    query.answer()
    reply_current_weather_result(query, context)


def bot_main():
    updater = Updater(BOT_HASH)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('user_options', user_options))
    dp.add_handler(MessageHandler(filters=telegram.ext.filters.Filters.text, callback=reply_current_weather_result))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    bot_main()
