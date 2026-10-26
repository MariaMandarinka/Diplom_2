import pytest
from helpers import StellarBurgersAPI, UserGenerator, StellarBurgersOrderAPI

@pytest.fixture
def unique_user_data():
    """Фикстура вызывает метод генерации данных из модуля helpers"""
    return UserGenerator.generate_user_data()

# НОВАЯ ФИКСТУРА ДЛЯ ТЕСТА УСПЕШНОЙ РЕГИСТРАЦИИ:
@pytest.fixture
def register_and_cleanup_user(unique_user_data):
    """Фикстура хранит токен создаваемого в тесте пользователя 
    и гарантированно удаляет его после окончания теста"""
    user_tokens = {}
    
    yield user_tokens  # Передаем пустой словарь в тест, тест заполнит его токеном
    
    # Блок очистки — выполнится в любом случае!
    token = user_tokens.get("accessToken")
    if token:
        StellarBurgersAPI.delete_user(token)

@pytest.fixture
def registered_user(unique_user_data):
    """Регистрация пользователя перед тестом и автоматическое удаление после"""
    response = StellarBurgersAPI.register_user(unique_user_data)
    token = response.json().get("accessToken")
    
    yield unique_user_data, token
    
    if token:
        StellarBurgersAPI.delete_user(token)
        # ДОБАВЛЯЕМ СЮДА ЭТУ ФИКСТУРУ ИЗ ТЕСТОВ ЗАКАЗА:
@pytest.fixture
def get_valid_ingredients():
    """Предусловие: Динамическое получение актуальных ID ингредиентов перед тестом"""
    resp = StellarBurgersOrderAPI.get_ingredients()
    # Возвращаем список из первых двух ID ингредиентов
    return [ing["_id"] for ing in resp.json()["data"][:2]]