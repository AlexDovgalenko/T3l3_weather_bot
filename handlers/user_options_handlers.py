from typing import TYPE_CHECKING

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import handlers
from bot_init import write_user_data
from general_emoji import GeneralEmojies
from keyboards.user_options_keyboards import reply_languages_keyboard, reply_weather_provider_keyboard

if TYPE_CHECKING:
    from aiogram import Dispatcher


class FSMUserOptions(StatesGroup):
    language = State()
    weather_provider = State()


async def settings(message: types.Message):
    await FSMUserOptions.language.set()
    keyboard = reply_languages_keyboard()
    await message.delete()
    await message.bot.send_message(text=f"{GeneralEmojies.BULLET_MARK.value} Будьласка оберіть мову:",
                                   reply_markup=keyboard, chat_id=message.chat.id)


# catch language reply
async def select_language(callback_data: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        data['language'] = callback_data.data
    await FSMUserOptions.next()
    await callback_data.message.edit_text(text=f"{GeneralEmojies.BULLET_MARK.value} "
                                               f"Будьласка оберіть провайдера погоди:",
                                          reply_markup=reply_weather_provider_keyboard())
    await callback_data.answer()


# catch weather provider reply
# @dp.message_handler(Text(equals=crossed_flags_emoji, ignore_case=True), state=FSMUserOptions.weather_provider)
async def select_weather_provides(callback_data: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        data['weather_provider'] = callback_data.data
    async with state.proxy() as data:
        write_user_data(user_id=callback_data.message.chat.id, user_data=data)
    await state.finish()
    await callback_data.message.edit_text("Налаштування закінчено!", reply_markup=None)
    await handlers.commands_handlers.start(callback_data.message)


def register_user_options_handlers(dispatcher: "Dispatcher"):
    # dispatcher.register_message_handler(options_config_start, Text(equals=options_emoji, ignore_case=True), state=None)
    dispatcher.register_message_handler(settings, commands="settings", state=None)
    dispatcher.register_callback_query_handler(select_language, state=FSMUserOptions.language)
    dispatcher.register_callback_query_handler(select_weather_provides, state=FSMUserOptions.weather_provider)
