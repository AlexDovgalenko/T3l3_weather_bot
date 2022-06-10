from aiogram import types
from aiogram.dispatcher.filters import Text

from bot_init import get_user_data
from keyboards.weather_keyboards import weather_forecast_type
from weather_operations import compile_current_weather_output


async def general_text_handler(message: types.Message):
    keyboard = weather_forecast_type()
    message_text = message.text
    await message.delete()
    await message.reply(text=message_text, reply_markup=keyboard, allow_sending_without_reply=True)


async def weather_choice_handler(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_data = get_user_data(chat_id)
    if callback_query.data == "_forecast_weather_current":
        weather_text = compile_current_weather_output(city_name=callback_query.message.text,
                                                      weather_provider_name=user_data[2])
        await callback_query.bot.send_message(text=weather_text, chat_id=chat_id)
    elif callback_query.data == "_forecast_weather_five_days":
        await callback_query.answer(text="Нажаль ця функці знаходиться у стадії розробки...")


def register_general_handlers(dispatcher: "Dispatcher"):
    dispatcher.register_callback_query_handler(weather_choice_handler, Text(startswith="_forecast_weather_"))
    dispatcher.register_message_handler(general_text_handler)
