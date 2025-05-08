import pytest
from main.models import TelegramUser

@pytest.fixture
def telegram_user_factory(db):
    def create_user(**kwargs):
        return TelegramUser.objects.create(**kwargs)
    return create_user

