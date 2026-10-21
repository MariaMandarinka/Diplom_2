class URL:
    """Базовый URL и эндпоинты для API Stellar Burgers"""
    # Актуальный базовый URL из документации диплома
    BASE_URL = "https://qa-stellarburgers.education-services.ru"

# Эндпоинты для работы с пользователем
class Endpoints:

    CREATE_USER = '/api/auth/register'
    LOGIN = '/api/auth/login'
    DELETE_USER = '/api/auth/user'
    CREATE_ORDER = '/api/orders'
    GET_ORDERS = '/api/orders'
    DATA_CHANGE = '/api/auth/user'

class StatusCode:
    """Статус коды"""

    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

# ДОПИШИТЕ ЭТИ СТРОКИ СЮДА:
class TestData:
    """Данные для негативных сценариев"""
    INVALID_INGREDIENTS_HASHES = ["invalid_hash_61c0c5b71d1f82001bda1234"]