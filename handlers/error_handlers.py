from aiogram import Dispatcher, types

import handlers.commands_handlers
from general_symbols import GeneralEmojis
from geocoding.geocoding_exceptions import GeneralGeocodingError


async def not_implemented_error_handler(update: types.Update, exception=NotImplementedError):
    """Handles NotImplementedError exception and throws pop-up message."""
    await update.callback_query.answer(text="Нажаль ця функці знаходиться у стадії розробки...", show_alert=True)
    await handlers.commands_handlers.start(update.callback_query.message)


async def geocoding_error_handler(update: types.Update, exception=GeneralGeocodingError):
    """Handling geocoding type of exceptions within bot app

    :param update: Update
    :param exception: Any GeneralGeocodingError type exception
    :return: warning message in the reply to user request
    """
    await update.message.reply(
        text=f"{GeneralEmojis.WARNING.value} Не вдалося визначити назву населеного пункту <b>'{update.message.text}'"
             f"</b>!\nПеревірте назву, та повторіть спробу!\n({exception})", allow_sending_without_reply=True)



async def global_error_handler(update: types.Update, exception):
    """Handling general exceptions within bot app

    :param update: Update
    :param exception: Exception any exception type
    :return: warning message in the reply to user request
    """
    await update.callback_query.message.delete_reply_markup()
    await update.callback_query.message.reply(
        f"{GeneralEmojis.WARNING.value} Сталася неочікувана помилка!!!\n"
        f"Перевірте назву населенного пункту, та повторіть спробу!\n({exception})")


def register_error_handlers(dispatcher: "Dispatcher"):
    dispatcher.errors_handlers.once = True
    dispatcher.register_errors_handler(not_implemented_error_handler, exception=NotImplementedError)
    dispatcher.register_errors_handler(geocoding_error_handler)
    dispatcher.register_errors_handler(global_error_handler)
