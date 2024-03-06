import pytest
from create_data import *
import allure
from urls import Urls

class TestGetOrderList:

    @allure.title('Проверка успешного получения списка заказов')
    @allure.description('Отправляется запрос на получение списка заказов. Проверяется код ответа, наличие orders в ответе и список всех ключей в теле ответа')
    def test_get_order_list(self):
        response = requests.get(f'{Urls.samokat_page}/api/v1/orders')
        order_keys = ['id', 'courierId', 'firstName', 'lastName', 'address', 'metroStation', 'phone', 'rentTime', 'deliveryDate', 'track', 'color', 'comment', 'createdAt', 'updatedAt', 'status']
        assert response.status_code == 200 and 'orders' in response.json() and list(response.json()["orders"][0].keys()) == order_keys
