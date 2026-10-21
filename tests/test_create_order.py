import pytest
import allure
from helpers import StellarBurgersOrderAPI
from data import StatusCode, TestData

@allure.feature("Создание заказа")
class TestOrderCreation:

    @pytest.fixture(autouse=True)
    def get_valid_ingredients(self):
        """Предусловие: Динамическое получение актуальных ID ингредиентов перед каждым тестом"""
        with allure.step("Запрос списка доступных ингредиентов у API"):
            resp = StellarBurgersOrderAPI.get_ingredients()
            self.valid_ids = [ing["_id"] for ing in resp.json()["data"][:2]]

    @allure.story("Создание бургера")
    @allure.title("Создание заказа с авторизацией")
    def test_create_order_authorized_success(self, registered_user):
        _, token = registered_user
        
        with allure.step("Отправка запроса на заказ с токеном авторизации"):
            response = StellarBurgersOrderAPI.create_order(self.valid_ids, token=token)
        
        with allure.step("Проверка успешного создания заказа для пользователя"):
            assert response.status_code == StatusCode.OK
            assert response.json()["success"] is True
            assert "order" in response.json()

    @allure.story("Создание бургера")
    @allure.title("Создание заказа без авторизации")
    def test_create_order_unauthorized_success(self):
        with allure.step("Отправка запроса на заказ без токена"):
            response = StellarBurgersOrderAPI.create_order(self.valid_ids, token=None)
        
        with allure.step("Проверка, что неавторизованный заказ успешно создается"):
            assert response.status_code == StatusCode.OK
            assert response.json()["success"] is True
            assert "order" in response.json()

    @allure.story("Создание бургера")
    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients_success(self, registered_user):
        _, token = registered_user
        
        with allure.step("Проверка успешной отправки заполненного массива ингредиентов"):
            response = StellarBurgersOrderAPI.create_order(self.valid_ids, token=token)
        
        assert response.status_code == StatusCode.OK
        assert response.json()["success"] is True

    @allure.story("Создание бургера")
    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_empty_ingredients_bad_request(self, registered_user):
        _, token = registered_user
        
        with allure.step("Отправка запроса на создание заказа с пустым массивом"):
            response = StellarBurgersOrderAPI.create_order(ingredients_list=[], token=token)
        
        with allure.step("Проверка статус-кода 400 и текста ошибки"):
            assert response.status_code == StatusCode.BAD_REQUEST
            assert response.json()["success"] is False
            assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.story("Создание бургера")
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_hash_internal_error(self, registered_user):
        _, token = registered_user
        
        with allure.step("Отправка запроса с заведомо некорректным ID ингредиента"):
            response = StellarBurgersOrderAPI.create_order(TestData.INVALID_INGREDIENTS_HASHES, token=token)
        
        with allure.step("Проверка падения сервера с ошибкой 500"):
            assert response.status_code == StatusCode.INTERNAL_SERVER_ERROR