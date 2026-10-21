import pytest
import allure
from helpers import StellarBurgersAPI
from data import StatusCode

@allure.feature("Создание пользователя")
class TestUserRegistration:
    
    @allure.story("Регистрация")
    @allure.title("Создать уникального пользователя")
    def test_register_unique_user_success(self, unique_user_data):
        with allure.step("Отправка запроса на регистрацию с уникальными данными"):
            response = StellarBurgersAPI.register_user(unique_user_data)
        
        with allure.step("Проверка успешного статус-кода 200 и флага успеха"):
            assert response.status_code == StatusCode.OK
            assert response.json()["success"] is True
            assert "accessToken" in response.json()
        
        with allure.step("Очистка: удаление созданного пользователя"):
            token = response.json()["accessToken"]
            StellarBurgersAPI.delete_user(token)

    @allure.story("Регистрация")
    @allure.title("Создать пользователя, который уже зарегистрирован")
    def test_register_existing_user_forbidden(self, registered_user):
        user_data, _ = registered_user
        
        with allure.step("Отправка повторного запроса на регистрацию с теми же данными"):
            response = StellarBurgersAPI.register_user(user_data)
        
        with allure.step("Проверка статус-кода 403 и сообщения об ошибке"):
            assert response.status_code == StatusCode.FORBIDDEN
            assert response.json()["success"] is False
            assert response.json()["message"] == "User already exists"

    @allure.story("Регистрация")
    @allure.title("Создать пользователя и не заполнить одно из обязательных полей")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_register_missing_field_forbidden(self, unique_user_data, missing_field):
        with allure.step(f"Удаление обязательного поля '{missing_field}' из тела запроса"):
            del unique_user_data[missing_field]
            
        with allure.step("Отправка запроса с незаполненным полем"):
            response = StellarBurgersAPI.register_user(unique_user_data)
        
        with allure.step("Проверка статус-кода 403 и текста ошибки валидации"):
            assert response.status_code == StatusCode.FORBIDDEN
            assert response.json()["success"] is False
            assert response.json()["message"] == "Email, password and name are required fields"