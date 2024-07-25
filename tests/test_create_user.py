
import allure
import pytest
import requests

from endpoints import Url, Endpoints


@allure.suite('Создание нового пользователя')
class TestCreateUser:

    @allure.title('Успешное создание пользователя')
    def test_create_new_user(self, register_new_user_return_response):
            email, password, name, response = register_new_user_return_response

            assert response.status_code == 200 and response.json() == {
                "success": True,
                "user": {
                    "email": email,
                    "name": name
                },
                "accessToken": response.json()["accessToken"],
                "refreshToken": response.json()["refreshToken"]
            }

    @allure.title('Повторная регистрация существующего пользователя')
    def test_register_created_user(self, register_new_user_return_response
):
        email, password, name, _ = register_new_user_return_response

        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(f'{Url.BASE_URL}{Endpoints.REGISTER_USER}', data=payload)

        assert response.status_code == 403 and response.json() == {"success": False, "message": "User already exists"}

    @allure.title('Регистрация пользователя c пропущенным обязательным полем {deleted_field}')
    @pytest.mark.parametrize('deleted_field', ['email', 'password', 'name'])
    def test_register_new_user_without_required_field(self, register_new_user_return_response, deleted_field):
        data = register_new_user_return_response
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
