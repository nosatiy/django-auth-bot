import asyncio
from django.core.management.base import BaseCommand
from django.conf import settings
from telebot.async_telebot import AsyncTeleBot
from main.telegram_bot.commands_handler import handle_start

bot = AsyncTeleBot(settings.BOT_TOKEN)


def register_handlers():
    bot.register_message_handler(handle_start, commands=["start"], pass_bot=True)


register_handlers()


async def run():
    await bot.polling(non_stop=True)


class Command(BaseCommand):
    help = "Run the Telegram bot"

    def handle(self, *args, **options):
        self.stdout.write("Starting Telegram bot...")
        asyncio.run(run())
