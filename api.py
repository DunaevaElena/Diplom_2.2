
import allure
import requests
from faker import Faker
from endpoints import Url, Endpoints
from helpers import generate_random_string

faker = Faker()


def create_new_user():
    login_pass = []

    email = faker.email()
    password = generate_random_string(10)
    username = faker.name()

    payload = {
        "email": email,
        "password": password,
        "name": username
    }

    response = requests.post(f"{Url.BASE_URL}{Endpoints.REGISTER_USER}", data=payload)

    if response.status_code == 200:
        login_pass.append(email)
        login_pass.append(password)
        login_pass.append(username)

    return login_pass, response
