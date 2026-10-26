import allure
from helpers import StellarBurgersAPI
from data import StatusCode
from faker import Faker

fake = Faker()

@allure.feature("Авторизация пользователя")
class TestUserLogin:

    @allure.story("Логин")
    @allure.title("Вход под существующим пользователем")
    # Убрали self из аргументов
    def test_login_existing_user_success(self, registered_user):
        user_data, _ = registered_user
        credentials = {"email": user_data["email"], "password": user_data["password"]}
        
        with allure.step("Отправка запроса на авторизацию с валидными данными"):
            response = StellarBurgersAPI.login_user(credentials)
        
        with allure.step("Проверка успешного логина (200 OK) и получения токенов"):
            assert response.status_code == StatusCode.OK
            assert response.json()["success"] is True
            assert "accessToken" in response.json()

    @allure.story("Логин")
    @allure.title("Вход с неверным логином и паролем")
    # Убрали self из аргументов
    def test_login_wrong_credentials_unauthorized(self):
        wrong_credentials = {"email": fake.email(), "password": fake.password()}
        
        with allure.step("Отправка запроса с несуществующими учетными данными"):
            # Выровняли отступ ровно под with!
            response = StellarBurgersAPI.login_user(wrong_credentials)
        
        with allure.step("Проверка статус-кода 401 и актуального сообщения об ошибке"):
            assert response.status_code == StatusCode.UNAUTHORIZED
            assert response.json()["success"] is False
            assert response.json()["message"] == "email or password are incorrect"