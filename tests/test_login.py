
import pytest
import requests
import allure
from faker import Faker

from endpoints import Url, Endpoints


@allure.suite('Авторизация пользователя')
class TestLoginUser:

    @allure.title('Авторизация существующего пользователя')
    def test_login_registered_user_success(self, register_new_user_return_response):
        data = register_new_user_return_response
        payload = {
            "email": data[0],
            "password": data[1]
        }
        response = requests.post(f'{Url.BASE_URL}{Endpoints.LOGIN}', data=payload)
        email = response.json()["user"]["email"]
        name = response.json()["user"]["name"]
        access_token = response.json()["accessToken"]
        refresh_token = response.json()["refreshToken"]

        assert response.status_code == 200 and response.text == \
               f'{{"success":true,"accessToken":"{access_token}","refreshToken":"{refresh_token}",' \
               f'"user":{{"email":"{email}","name":"{name}"}}}}'

    @allure.title('Авторизация с некорректным {email}')
    @pytest.mark.parametrize('email', ['faker.email()', ' '], ids=['incorrect_email', 'empty_email'])
    def test_login_user_incorrect_email_and_correct_password(self, register_new_user_return_response,
                                                             email):
        faker = Faker()
        data = register_new_user_return_response
        payload = {
            "email": email,
            "password": data[1]
        }
        response = requests.post(f'{Url.BASE_URL}{Endpoints.LOGIN}', data=payload)
        assert response.status_code == 401 and response.text == \
               '{"success":false,"message":"email or password are incorrect"}'

    @allure.title('Авторизация с некорректным {password}')
    @pytest.mark.parametrize('password', ['faker.password()', ' '], ids=['incorrect password', 'empty password'])
    def test_login_user_correct_email_incorrect_password(self, register_new_user_return_response, password):
        faker = Faker()
        data = register_new_user_return_response
        payload = {
            "email": data[0],
            "password": password
        }
        response = requests.post(f'{Url.BASE_URL}{Endpoints.LOGIN}', data=payload)
        assert response.status_code == 401 and response.text == \
               '{"success":false,"message":"email or password are incorrect"}'
