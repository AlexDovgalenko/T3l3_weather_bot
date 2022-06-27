from typing import TYPE_CHECKING

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Regexp
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_init import get_user_data
from geocoding.geocoding_utils import get_available_location_options
from keyboards.general_keyboards import weather_forecast_type_keyboard, city_specification_items_keyboard
from weather_operations import compile_weather_output

if TYPE_CHECKING:
    from aiogram import Dispatcher


class FSMWeatherConditions(StatesGroup):
    lat_lon = State()
    forecast_type = State()


async def general_text_handler(message: types.Message, state=None):
    """Handles all messages from user."""
    message_text = message.text
    await message.delete()
    available_location_options = get_available_location_options(message_text)
    if len(available_location_options) > 1:
        keyboard = city_specification_items_keyboard(available_location_options)
        await FSMWeatherConditions.lat_lon.set()
        await message.reply(text=message_text, reply_markup=keyboard, allow_sending_without_reply=True)

    else:
        async with state.proxy() as data:
            data['lat_lon'] = available_location_options[0].lat_lon
        keyboard = weather_forecast_type_keyboard()
        await message.reply(text=message_text, reply_markup=keyboard, allow_sending_without_reply=True)
        await FSMWeatherConditions.forecast_type.set()


async def location_choice_handler(callback_query: types.CallbackQuery, state=FSMContext):
    """Handles user choice of location on FSMWeatherConditions.lat_lon state."""
    # chat_id = callback_query.message.chat.id
    async with state.proxy() as data:
        data['lat_lon'] = callback_query.data
    keyboard = weather_forecast_type_keyboard()
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await FSMWeatherConditions.next()


async def weather_choice_handler(callback_query: types.CallbackQuery, state=FSMContext):
    """Handles user choice of weather forecast on FSMWeatherConditions.forecast_type state."""
    chat_id = callback_query.message.chat.id
    user_data = get_user_data(chat_id)
    async with state.proxy() as data:
        data['forecast_type'] = callback_query.data
    weather_options = data._data
    await state.finish()
    weather_text = compile_weather_output(city_name=callback_query.message.text,
                                          weather_provider_name=user_data[2],
                                          lat_lon=weather_options.get("lat_lon"),
                                          forecast_type=weather_options.get("forecast_type"))
    await callback_query.bot.send_message(text=weather_text, chat_id=chat_id)


def register_general_handlers(dispatcher: "Dispatcher"):
    """Registers all general handlers."""
    dispatcher.register_callback_query_handler(location_choice_handler,
                                               Regexp(regexp=r"\d{2}.\d.*-\d{2}.\d.*"),
                                               state=FSMWeatherConditions.lat_lon)
    dispatcher.register_callback_query_handler(weather_choice_handler, Text(startswith="_forecast_weather_"),
                                               state=FSMWeatherConditions.forecast_type)
    dispatcher.register_message_handler(general_text_handler, state=None)
