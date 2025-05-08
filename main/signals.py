from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User
from main.tasks.notify_on_login import send_telegram_notification
from datetime import datetime as dt


@receiver(user_logged_in)
def notify_on_login(sender: any, request: any, user: User, **kwargs):
    send_telegram_notification.send(user.username, str(dt.now()))
