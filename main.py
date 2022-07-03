from aiogram import executor
from loguru import logger
from configure_logging import configure_logger
from bot_init import dp
from handlers import user_options_handlers, commands_handlers, general_handlers, error_handlers

logger.remove(0)
configure_logger()


async def on_startup(_):
    logger.info("Bot went Online!!!")


error_handlers.register_error_handlers(dp)
commands_handlers.register_commands_handlers(dp)
user_options_handlers.register_user_options_handlers(dp)
general_handlers.register_general_handlers(dp)


def launch_bot():
    logger.info("Launching the bot...")
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    launch_bot()
