import requests
import pytest
from urls import Urls
from helpers import generate_random_string


@pytest.fixture
def register_new_courier():
    # Создаем курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        'login': login,
        'password': password,
        'firstName': first_name
    }

    # Выводим логин и пароль на экран
    print(f"Courier Login: {login}")
    print(f"Courier Password: {password}")

    response = requests.post(Urls.url_courier, data=payload)

    # Логинимся, чтобы получить ID курьера
    login_payload = {
        'login': login,
        'password': password
    }
    login_response = requests.post(Urls.url_courier_login, data=login_payload)
    login_data = login_response.json()
    courier_id = login_data.get('id')

    # Передаем данные курьера и его ID в тест
    yield response, payload, courier_id

    # Удаляем курьера после теста
    delete_response = requests.delete(f"{Urls.url_courier}/{courier_id}")


