import requests
import allure
from urls import Urls
from helpers import generate_random_string, register_new_courier_and_return_login_password


class TestCourierLogin:

    @allure.title('Проверка успешной авторизации курьера при вводе валидных данных')
    @allure.description('Создаем нового курьера с рандомными данными и логинимся c ними в системе. Проверяем код и тело ответа.')
    def test_courier_login_success(self):
        login_pass = register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = login_pass[1]

        payload = {
            'login': login,
            'password': password
        }

        response = requests.post(Urls.url_courier_login, data=payload)
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        response_json = response.json()
        assert 'id' in response_json, "Response does not contain 'id'"

    @allure.title('Проверка получения ошибки аутентификации курьера при вводе некорректного пароля.')
    @allure.description('Создаем курьера с валидными данными, регистрируемся с корректным логином и некорректным паролем. Проверяются код и тело ответа.')
    def test_courier_login_wrong_password(self):
        login_pass = register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = generate_random_string(10)

        payload = {
            'login': login,
            'password': password
        }
        response = requests.post(Urls.url_courier_login, data=payload)
        assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
        assert response.json() == {'message': 'Учетная запись не найдена'}, f"Unexpected response: {response.json()}"


    @allure.title('Проверка получения ошибки аутентификации курьера при вводе некорректного логина.')
    @allure.description('Создаем курьера с валидными данными, регистрируемся с некорректным логином и корректным паролем. Проверяются код и тело ответа.')
    def test_courier_login_wrong_login(self):
        login_pass = register_new_courier_and_return_login_password()
        login = generate_random_string(10)
        password = login_pass[1]

        payload = {
            'login': login,
            'password': password
        }
        response = requests.post(Urls.url_courier_login, data=payload)
        assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
        assert response.json() == {'message': 'Учетная запись не найдена'}, f"Unexpected response: {response.json()}"

    @allure.title('Проверка получения ошибки аутентификации курьера с пустым полем логина')
    @allure.description('В тест передаётся набор данных с пустым логином. Проверяются код и тело ответа.')
    def test_courier_login_empty_login(self):
        login_pass = register_new_courier_and_return_login_password()
        login = ''
        password = login_pass[1]

        payload = {
            'login': login,
            'password': password
        }
        response = requests.post(Urls.url_courier_login, data=payload)
        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert response.json() == {
            'message': 'Недостаточно данных для входа'}, f"Unexpected response: {response.json()}"


    @allure.title('Проверка получения ошибки аутентификации курьера с пустым полем пароля')
    @allure.description('В тест передаётся набор данных с пустым паролем. Проверяются код и тело ответа.')
    def test_courier_login_empty_password(self):
        login_pass = register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = ''

        payload = {
            'login': login,
            'password': password
        }
        response = requests.post(Urls.url_courier_login, data=payload)
        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert response.json() == {'message': 'Недостаточно данных для входа'}, f"Unexpected response: {response.json()}"
