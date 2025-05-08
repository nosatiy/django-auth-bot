import dramatiq
from telebot.async_telebot import AsyncTeleBot
from main.models import TelegramUser
from dotenv import load_dotenv
from django.conf import settings
from asgiref.sync import sync_to_async
import asyncio

load_dotenv()
bot = AsyncTeleBot(settings.BOT_TOKEN)

@sync_to_async
def get_chat_ids():
    return list(TelegramUser.objects.values_list("chat_id", flat=True))

@dramatiq.actor
def send_telegram_notification(username: str, time: str):
    asyncio.run(_send(username, time))

async def _send(username: str, time: str):
    text = f"Пользователь {username} вошел в {time}"
    
    chat_ids = await get_chat_ids()
    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id, text)
        except Exception as e:
            print(f"Ошибка отправки в Telegram: {e}")
