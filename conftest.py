
import allure
import pytest
import requests
from pip._internal.utils import logging

from endpoints import Url, Endpoints
import api
logger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def register_new_user_return_response():
    with allure.step('Получение данных о зарегистрированном пользователе'):
        user_data, response = api.create_new_user()

        yield user_data[0], user_data[1], user_data[2], response

    with allure.step('Получение токена созданного пользователя'):
        access_token = response.json()["accessToken"]

    with allure.step('Удаление созданного пользователя'):
        requests.delete(f"{Url.BASE_URL}{Endpoints.DELETE_USER}", headers={'Authorization': f'{access_token}'})
