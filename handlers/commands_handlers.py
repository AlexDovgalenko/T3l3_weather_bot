from aiogram import types

from bot_init import dp, get_all_user_ids
from handlers.user_options_handlers import settings

start_text = "<b>Оберіть назву населеного пункту...</b>"

about_text = """Цей бот дозволяє дізнатися <b>поточну погоду</b> в обраному населеному пункті або <b>прогноз ну найближчі 5 днів</b> за бажанням.
Провайдера погоди можна обрати у <b>налаштуваннях</b> бота.
Щоб змінити <b>налаштування</b> бота оберіть відповідний пункт меню."""


@dp.message_handler(commands='start')
async def start(message: types.Message):
    chat_id = message.chat.id
    if chat_id in get_all_user_ids():
        # move to forecast view
        await message.delete()
        await message.reply(text=start_text, allow_sending_without_reply=True)
    else:
        # proceed with user options configuration
        await settings(message=message)


@dp.message_handler(commands='about')
async def about(message: types.Message):
    await message.delete()
    await message.reply(text=about_text, allow_sending_without_reply=True)


def register_commands_handlers(dispatcher: "Dispatcher"):
    dispatcher.register_message_handler(start, commands="start")
    dispatcher.register_message_handler(about, commands="about")

