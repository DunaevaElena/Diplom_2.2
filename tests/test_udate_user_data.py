import allure
import pytest
import requests
from faker import Faker

from endpoints import Url, Endpoints


@allure.suite('Изменение данных пользователя')
class TestUpdateUserData:

    @allure.title('Изменение данных авторизованного пользователя')
    @pytest.mark.parametrize('changed_data', [lambda data, fake: {"email": fake.email(), "password": data[1], "name": data[2]},
        lambda data, fake: {"email": data[0], "password": fake.password(), "name": data[2]},
        lambda data, fake: {"email": data[0], "password": data[1], "name": fake.name()},
    ], ids=['email', 'password', 'name'])
    def test_update_authorized_user(self, register_new_user_return_response, changed_data):
        data = register_new_user_return_response
        fake = Faker()
        payload = changed_data(data, fake)
        access_token = data[3].json()['accessToken']
        headers = {"Authorization": f"{access_token}"}
        response = requests.patch(f'{Url.BASE_URL}{Endpoints.UPDATE_USER}', json=payload, headers=headers)
        email = response.json()['user']['email']
        name = response.json()['user']['name']

        assert response.status_code == 200 and response.json() == {
            "success": True,
            "user": {
                "email": email,
                "name": name
            }
        }

    @allure.title('Изменение данных для не авторизованного пользователя')
    @pytest.mark.parametrize('changed_data', ['{"email": fake.email(), "password": data[1],"name": data[2]}',
                                              '{"email": data[0], "password": fake.password(), "name": data[2]}',
                                              '{"email": data[0], "password":data[1], "name":fake.name()}'],
                             ids=['email', 'password', 'name'])
    def test_update_info_non_authorized_user(self, register_new_user_return_response, changed_data):
        data = register_new_user_return_response
        fake = Faker()
        payload = changed_data
        response = requests.patch(f'{Url.BASE_URL}{Endpoints.UPDATE_USER}', data=payload)

        assert response.status_code == 401 and response.text == \
               '{"success":false,"message":"You should be authorised"}'

    @allure.title('Изменение email')
    def test_changed_email_to_email_already_used(self, register_new_user_return_response):
        data = register_new_user_return_response
        payload = {"email": "test-data@yandex.ru"}
        access_token = data[3].json()['accessToken']
        headers = {"Authorization": f"{access_token}"}
        response = requests.patch(f'{Url.BASE_URL}{Endpoints.UPDATE_USER}', data=payload, headers=headers)

        assert response.status_code == 403 and response.text == \
               '{"success":false,"message":"User with such email already exists"}'