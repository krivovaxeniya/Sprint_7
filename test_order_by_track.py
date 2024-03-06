import pytest
from create_data import *
import json
import allure
from urls import Urls

class TestGetOrderByTrack:

    @allure.title('Проверка успешного получения заказа по номеру')
    @allure.description('Создается заказ, получается его track-номер. Полученный номер отправляется в запрос для получения информации по заказу. Проверяется код ответа, наличие order в ответе и список всех ключей в теле ответа')
    def test_get_order_by_track(self):
        payload_order = {"firstName": 'Naruto',
                         "lastName": 'Uchiha',
                         "address": 'Konoha, 142 apt.',
                         "metroStation": '4',
                         "phone": '+7 800 355 35 35',
                         "rentTime": 5,
                         "deliveryDate": '2020-06-06',
                         "comment": 'Saske, come back to Konoha',
                         "color": [
                                   'BLACK']}
        payload_string = json.dumps(payload_order)
        response_order = requests.post(f'{Urls.samokat_page}/api/v1/orders', data=payload_string)
        track_order = response_order.json()['track']
        payload = {"t": track_order}
        response = requests.get(f'{Urls.samokat_page}/api/v1/orders/track?t={track_order}', data=payload)
        order_keys = ['id', 'firstName', 'lastName', 'address', 'metroStation', 'phone', 'rentTime', 'deliveryDate', 'track', 'color', 'comment', 'cancelled', 'finished', 'inDelivery', 'courierFirstName', 'createdAt', 'updatedAt']
        assert response.status_code == 200 and 'order' in response.json() and list(response.json()["order"].keys()) == order_keys #тест падает по причине того, что ключи ответа не соответствуют ожидаемым в требованиях

    @allure.title('Проверка отсутствия получения заказа при некорректном номере')
    @allure.description('Создается заказ, получается его track-номер. Номер, отличный от полученного, отправляется в запрос для получения информации по заказу. Проверяется код ответа и сообщение об ошибке')
    def test_get_order_with_incorrect_track(self):
        payload_order = {"firstName": 'Naruto',
                         "lastName": 'Uchiha',
                         "address": 'Konoha, 142 apt.',
                         "metroStation": '4',
                         "phone": '+7 800 355 35 35',
                         "rentTime": 5,
                         "deliveryDate": '2020-06-06',
                         "comment": 'Saske, come back to Konoha',
                         "color": [
                                   'BLACK']}
        payload_string = json.dumps(payload_order)
        response_order = requests.post(f'{Urls.samokat_page}/api/v1/orders', data=payload_string)
        track_order = f'{response_order.json()["track"]}1'
        payload = {"t": track_order}
        response = requests.get(f'{Urls.samokat_page}/api/v1/orders/track?t={track_order}', data=payload)
        assert response.status_code == 404 and 'Заказ не найден' in response.json()['message']

    @allure.title('Проверка отсутствия получения заказа при незаполненном номере')
    @allure.description('Отправляется запрос для получения информации по заказу с незаполненным номером. Проверяется код ответа и сообщение об ошибке')
    def test_get_order_without_track(self):
        track_order = ""
        payload = {"t": track_order}
        response = requests.get(f'{Urls.samokat_page}/api/v1/orders/track?t={track_order}',
                                data=payload)
        assert response.status_code == 400 and 'Недостаточно данных для поиска' in response.json()['message']
