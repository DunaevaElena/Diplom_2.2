
import allure
import pytest
import requests
from faker.proxy import Faker
from pip._internal.utils import logging

from endpoints import Url, Endpoints
import api
logger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def register_new_user_return_response():
    with allure.step('Получение данных о зарегистрированном пользователе'):
        data = api.create_new_user()

        yield data[1]

    with allure.step('Получение токена созданного пользователя'):
        access_token = data[1].json()["accessToken"]
    with allure.step('Удаление созданного пользователя'):
        requests.delete(f"{Url.BASE_URL}{Endpoints.DELETE_USER}", headers={'Authorization': f'{access_token}'})


@pytest.fixture(scope='function')
def register_new_user_return_login_and_password():
    with allure.step('Получение логина и пароля зарегистрированного пользователя'):
        data = api.create_new_user()

        yield data[0]

    with allure.step('Получение токена созданного пользователя'):
        access_token = data[1].json()["accessToken"]
    with allure.step('Удаление созданного пользователя'):
        requests.delete(f"{Url.BASE_URL}{Endpoints.DELETE_USER}", headers={'Authorization': f'{access_token}'})

@pytest.fixture()
def new_user(user_endpoints, payload_for_create_user):
    logger.info('+=fixture - new_user=+')
    user_endpoints.create_user(payload_for_create_user)
    access_token = user_endpoints.access_token
    user = {
        "email": payload_for_create_user['email'],
        "password": payload_for_create_user['password'],
        "name": payload_for_create_user['name'],
        "access_token": access_token
    }
    yield user

    if access_token is not None:
        headers = {"Authorization": access_token}
        user_endpoints.delete_user(headers)

@pytest.fixture()
def user_endpoints():
    return Endpoints()

@pytest.fixture()
def payload_for_create_user():
    fake = Faker()
    payload = {
        "email": f'testuser{fake.email()}',
        "password": fake.password(),
        "name": fake.user_name()
    }
    return payload