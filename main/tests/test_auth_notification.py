import pytest
from unittest.mock import AsyncMock, patch
from main.tasks.notify_on_login import send_telegram_notification  # Импортируем функцию для тестирования

@pytest.mark.django_db
@patch("main.tasks.notify_on_login.bot.send_message", new_callable=AsyncMock)
def test_send_telegram_notification(mock_send_message):
    with patch("main.tasks.notify_on_login.TelegramUser.objects.values_list") as mock_values_list:
        mock_values_list.return_value = ["test_chat_id"]

        send_telegram_notification("test_user", "2025-05-08 15:59:08")

        mock_send_message.assert_called_once_with(
            "test_chat_id", 
            "Пользователь test_user вошел в 2025-05-08 15:59:08"
        )

@pytest.mark.django_db
@patch("main.tasks.notify_on_login.bot.send_message", new_callable=AsyncMock)
def test_send_telegram_notification_no_chat_ids(mock_send_message):
    with patch("main.tasks.notify_on_login.TelegramUser.objects.values_list") as mock_values_list:
        mock_values_list.return_value = []
        send_telegram_notification("test_user", "2025-05-08 15:59:08")
        mock_send_message.assert_not_called()

@pytest.mark.django_db
@patch("main.tasks.notify_on_login.bot.send_message", new_callable=AsyncMock)
def test_send_telegram_notification_multiple_chat_ids(mock_send_message):
    with patch("main.tasks.notify_on_login.TelegramUser.objects.values_list") as mock_values_list:
        mock_values_list.return_value = ["chat_id_1", "chat_id_2"]
        send_telegram_notification("test_user", "2025-05-08 15:59:08")
        mock_send_message.assert_any_call("chat_id_1", "Пользователь test_user вошел в 2025-05-08 15:59:08")
        mock_send_message.assert_any_call("chat_id_2", "Пользователь test_user вошел в 2025-05-08 15:59:08")

@pytest.mark.django_db
@patch("main.tasks.notify_on_login.bot.send_message", new_callable=AsyncMock)
def test_send_telegram_notification_handle_error(mock_send_message):
    with patch("main.tasks.notify_on_login.TelegramUser.objects.values_list") as mock_values_list:
        mock_values_list.return_value = ["chat_id_1"]
        mock_send_message.side_effect = Exception("Ошибка при отправке сообщения")
        send_telegram_notification("test_user", "2025-05-08 15:59:08")
        mock_send_message.assert_called_once_with("chat_id_1", "Пользователь test_user вошел в 2025-05-08 15:59:08")

@pytest.mark.django_db
@patch("main.tasks.notify_on_login.bot.send_message", new_callable=AsyncMock)
def test_send_telegram_notification_async(mock_send_message):
    with patch("main.tasks.notify_on_login.TelegramUser.objects.values_list") as mock_values_list:
        mock_values_list.return_value = ["chat_id_1"]
        send_telegram_notification("test_user", "2025-05-08 15:59:08")
        mock_send_message.assert_awaited_once_with("chat_id_1", "Пользователь test_user вошел в 2025-05-08 15:59:08")
