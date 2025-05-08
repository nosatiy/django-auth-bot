from asgiref.sync import sync_to_async
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot
from django.db import IntegrityError
from main.models import TelegramUser


async def handle_start(message: Message, bot: AsyncTeleBot):
    print("Handling /start command...")
    chat = message.chat

    user_exists = await sync_to_async(
        TelegramUser.objects.filter(chat_id=chat.id).exists
    )()
    print(f"User exists: {user_exists}")

    if user_exists:
        await bot.send_message(chat.id, "Вы уже подписаны.")
    else:
        try:
            await sync_to_async(TelegramUser.objects.create)(
                chat_id=chat.id,
                username=chat.username,
                first_name=chat.first_name,
                last_name=chat.last_name,
            )
            await bot.send_message(chat.id, "Вы успешно подписались на уведомления.")
        except IntegrityError:
            await bot.send_message(chat.id, "Произошла ошибка при подписке.")
