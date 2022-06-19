import logging

from aiogram import executor

# from telegram import Update, ParseMode, KeyboardButton, ReplyKeyboardMarkup
# from telegram.ext import CommandHandler, Updater, CallbackQueryHandler, CallbackContext, MessageHandler
from bot_init import dp
from handlers import user_options_handlers, commands_handlers, general_handlers, error_handlers

test_data = []

options_dict = {}

logging.basicConfig(
    format='%(asctime)s - [%(name)s] [%(levelname)s] - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


async def on_startup(_):
    logger.info("Bot went Online!!!")


error_handlers.register_error_handlers(dp)
commands_handlers.register_commands_handlers(dp)
user_options_handlers.register_user_options_handlers(dp)
general_handlers.register_general_handlers(dp)


def launch_bot():
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    launch_bot()
