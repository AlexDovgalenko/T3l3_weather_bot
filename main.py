import logging

from aiogram import executor, types

# from telegram import Update, ParseMode, KeyboardButton, ReplyKeyboardMarkup
# from telegram.ext import CommandHandler, Updater, CallbackQueryHandler, CallbackContext, MessageHandler
from bot_init import dp
from keyboards.common_emoji_codes import options_emoji, weather_forecast_emoji
from handlers import user_options_handlers, commands_handlers, general_handlers

test_data = []

options_dict = {}

logging.basicConfig(
    format='%(asctime)s - [%(name)s] [%(levelname)s] - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


async def on_startup(_):
    logger.info("Bot went Online!!!")

# def reply_current_weather_result(update: Update, context: CallbackContext):
#     chat_id = update.message.chat_id
#     message_id = update.message.message_id
#     weather_text = compile_current_weather_output(city_name=update.message.text, weather_provider=WEATHER_PROVIDER)
#     # keyboard = [[KeyboardButton(text="Оберіть назву населеного пункту...")]]
#     # reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True,)
#     # reply_markup = InlineKeyboardMarkup(keyboard)=
#     context.bot.send_message(text=weather_text, chat_id=chat_id, parse_mode=ParseMode.HTML)


# def reply_start_keyboard():
#     start_buttons = [options_emoji, weather_forecast_emoji]
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     keyboard.add(*start_buttons)
#     return keyboard


commands_handlers.register_commands_handlers(dp)
user_options_handlers.register_user_options_handlers(dp)
general_handlers.register_general_handlers(dp)


# @dp.message_handler(Text(equals="\U0001F6E0"))
# async def handle_user_options(  )


# def user_options(update: Update, _: CallbackContext) -> None:
#     chat_id = update.message.chat_id
#     reply_markup = user_options_keyboard()
#     update.message.bot.send_message(text='Select a language', reply_markup=reply_markup, chat_id=chat_id)


def bot_main_test():
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    bot_main_test()
