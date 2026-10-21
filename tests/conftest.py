import pytest
from faker import Faker
from helpers import StellarBurgersAPI

fake = Faker()

@pytest.fixture
def unique_user_data():
    """Генерация случайных валидных данных пользователя"""
    return {
        "email": fake.email(),
        "password": fake.password(length=10),
        "name": fake.first_name()
    }

@pytest.fixture
def registered_user(unique_user_data):
    """Регистрация пользователя перед тестом и автоматическое удаление после"""
    response = StellarBurgersAPI.register_user(unique_user_data)
    token = response.json().get("accessToken")
    
    yield unique_user_data, token
    
    if token:
        StellarBurgersAPI.delete_user(token)