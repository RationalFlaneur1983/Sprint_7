import requests
import allure
from user_data import OrderData
from helpers import OrderHelper
from urls import Urls

class TestOrdersListGet:

    @allure.title('Проверка что при запросе списка заказов в теле ответа возвращается список')
    @allure.description('Создаем четыре заказа из user_data с разными параметрами, выводим список на экран. Проверяются код и тело ответа.')
    def test_orders_get_list(self):
        for order_data in [
            OrderData.order_data_grey,
            OrderData.order_data_black,
            OrderData.order_data_two_colors,
            OrderData.order_data_no_color
        ]:
            OrderHelper.create_orders(order_data)

        response = requests.get(Urls.url_orders_create)
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response: {response.text}"
        response_json = response.json()
        assert isinstance(response_json.get('orders'), list), f"'orders' is not a list. Response: {response_json}"