
import allure
import pytest
import requests

from endpoints import Url, Endpoints


@allure.suite('Создание нового пользователя')
class TestCreateUser:

    @allure.title('Успешное создание пользователя')
    def test_create_new_user(self, register_new_user_return_response):
        response = register_new_user_return_response

        email = response.json()["user"]["email"]
        name = response.json()["user"]["name"]
        access_token = response.json()["accessToken"]
        refresh_token = response.json()["refreshToken"]

        assert response.status_code == 200 and response.text == \
               f'{{"success":true,"user":{{"email":"{email}","name":"{name}"}},' \
               f'"accessToken":"{access_token}","refreshToken":"{refresh_token}"}}'

    @allure.title('Повторная регистрация существующего пользователя')
    def test_register_created_user(self, register_new_user_return_login_and_password
):
        data = register_new_user_return_login_and_password

        email = data[0]
        password = data[1]
        name = data[2]
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(f'{Url.BASE_URL}{Endpoints.REGISTER_USER}', data=payload)

        assert response.status_code == 403 and response.text == '{"success":false,"message":"User already exists"}'

    @allure.title('Регистрация пользователя c пропущенным обязательным полем {deleted_field}')
    @pytest.mark.parametrize('deleted_field', ['email', 'password', 'name'])
    def test_register_new_user_without_required_field(self, register_new_user_return_login_and_password, deleted_field):
        data = register_new_user_return_login_and_password
        email = data[0]
        password = data[1]
        name = data[2]
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        del payload[deleted_field]
        response = requests.post(f'{Url.BASE_URL}{Endpoints.REGISTER_USER}', data=payload)
        assert response.status_code == 403 and response.text ==\
               '{"success":false,"message":"Email, password and name are required fields"}'
