import pytest
from create_data import *
import json
import allure
from urls import Urls


class TestCreateOrder:

    @allure.title('Проверка успешного создания заказа с различным значением параметра цвет')
    @allure.description('Отправляется запрос на создание заказа с меняющимся значением параметра цвет. Проверяется код ответа и наличие track в ответе')
    @pytest.mark.parametrize('color', ["BLACK", "GREY", ["BLACK", "GREY"], ""])
    def test_create_order(self, color):
        payload = {"firstName": "Naruto",
                   "lastName": "Uchiha",
                   "address": "Konoha, 142 apt.",
                   "metroStation": 4,
                   "phone": "+7 800 355 35 35",
                   "rentTime": 5,
                   "deliveryDate": "2020-06-06",
                   "comment": "Saske, come back to Konoha",
                   "color": [
                             color]}
        payload_string = json.dumps(payload)
        response = requests.post(f'{Urls.samokat_page}/api/v1/orders', data=payload_string)
        assert response.status_code == 201 and 'track' in response.text