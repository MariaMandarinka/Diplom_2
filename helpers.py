import requests
from data import URL, Endpoints

class StellarBurgersAPI:
    """Хелпер для работы с пользователем и авторизацией"""
    
    @staticmethod
    def register_user(user_data):
        return requests.post(f"{URL.BASE_URL}{Endpoints.CREATE_USER}", json=user_data)

    @staticmethod
    def login_user(credentials):
        return requests.post(f"{URL.BASE_URL}{Endpoints.LOGIN}", json=credentials)

    @staticmethod
    def delete_user(token):
        headers = {"Authorization": token} if token else {}
        return requests.delete(f"{URL.BASE_URL}{Endpoints.DELETE_USER}", headers=headers)


class StellarBurgersOrderAPI:
    """Хелпер для работы с заказами и ингредиентами"""

    @staticmethod
    def get_ingredients():
        # Ручка /api/ingredients обычно не меняется, берем её напрямую
        return requests.get(f"{URL.BASE_URL}/api/ingredients")

    @staticmethod
    def create_order(ingredients_list, token=None):
        headers = {"Authorization": token} if token else {}
        payload = {"ingredients": ingredients_list}
        return requests.post(f"{URL.BASE_URL}{Endpoints.CREATE_ORDER}", headers=headers, json=payload)