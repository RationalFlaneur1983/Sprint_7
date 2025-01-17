import requests
import allure
from urls import Urls
from helpers import generate_random_string, register_new_courier_and_return_login_password


class TestCourierCreate:

    @allure.title('Проверка успешного создания аккаунта курьера с валидными данными.')
    @allure.description('Создаем нового курьера с рандомными данными. Проверяем код и тело ответа')
    def test_create_courier_account(self):
        payload = {
            'login': generate_random_string(10),
            'password': generate_random_string(10),
            'firstName': generate_random_string(10)
        }
        response = requests.post(Urls.url_courier_create, data=payload)
        assert response.status_code == 201, f"Unexpected status code: {response.status_code}"
        assert response.json() == {'ok': True}, f"Unexpected response: {response.json()}"

    @allure.title('Проверка ошибки при повторном использовании логина для создания курьера.')
    @allure.description('Создаем нового курьера с рандомными данными и повторяем запрос на создание используя такой же логин. Проверяем код и тело ответа.')
    def test_create_courier_existing_login(self):
        login_pass = register_new_courier_and_return_login_password()
        login = login_pass[0]

        payload_duplicate = {
            'login': login,
            'password': generate_random_string(10),
            'firstName': generate_random_string(10)
        }

        response = requests.post(Urls.url_courier_create, data=payload_duplicate)

        assert response.status_code == 409, f"Unexpected status code: {response.status_code}"
        assert response.json() == {'message': "Этот логин уже используется"}, f"Unexpected response: {response.json()}"

    @allure.title('Проверка получения ошибки при создании курьера с незаполненным обязательным полем - логин')
    @allure.description('В тест передается набор обязательных данных без логина. Проверяем код и тело ответа.')
    def test_create_courier_account_with_empty_login(self):
        no_login = {'login': '', 'password': generate_random_string(10), 'firstName': generate_random_string(10)}
        response = requests.post(Urls.url_courier_create, data=no_login)
        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert response.json() == {'message': 'Недостаточно данных для создания учетной записи'}, f"Unexpected response: {response.json()}"

    @allure.title('Проверка получения ошибки при создании курьера с незаполненным обязательным полем - пароль')
    @allure.description('В тест передается набор обязательных данных без пароля. Проверяем код и тело ответа.')
    def test_create_courier_account_with_empty_password(self):
        no_pass = {'login': generate_random_string(10), 'password': '', 'firstName': generate_random_string(10)}
        response = requests.post(Urls.url_courier_create, data=no_pass)
        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert response.json() == {'message': 'Недостаточно данных для создания учетной записи'}, f"Unexpected response: {response.json()}"