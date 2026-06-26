from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, Message


async def safe_edit_message_text(
    bot: Bot,
    chat_id: int,
    message_id: int,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> None:
    try:
        await bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup,
        )
    except TelegramBadRequest as error:
        if 'message is not modified' not in str(error):
            raise


async def safe_edit_text(
    message: Message,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> None:
    try:
        await message.edit_text(
            text=text,
            reply_markup=reply_markup,
        )
    except TelegramBadRequest as error:
        if 'message is not modified' not in str(error):
            raise


async def safe_delete_message(message: Message) -> None:
    try:
        await message.delete()
    except TelegramBadRequest:
        return
