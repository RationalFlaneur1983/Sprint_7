import random
import string
import requests
import json
from urls import Urls

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


class OrderHelper:
    @staticmethod
    def create_orders(order_data):
        order_data_json = json.dumps(order_data)
        response = requests.post(Urls.url_orders_create, data=order_data_json)
        return response
