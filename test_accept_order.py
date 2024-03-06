import pytest
from create_data import *
import allure
from urls import Urls


class TestAcceptOrder:

    @allure.title('Проверка успешного принятия заказа для курьера')
    @allure.description('Используются методы создания курьера и заказа и получения их id. Полученные данные отправляются в запрос на принятие заказа. Проверяется код ответа и сообщение об успешном выполнении запроса')
    def test_accept_order_for_courier(self):
        id_courier = create_courier_and_return_id()
        id_order = create_order_and_return_id()
        payload = {"id": id_order,
                   "courierId": id_courier}
        response = requests.put(f'{Urls.samokat_page}/api/v1/orders/accept/{id_order}?courierId={id_courier}',
                                      data=payload)
        assert response.status_code == 200 and response.text == '{"ok":true}'

    @allure.title('Проверка отсутствия принятия заказа для курьера при некорректном id заказа')
    @allure.description('Используются методы создания курьера и заказа и получения их id. Полученный id курьера и измененный id заказа отправляются в запрос на принятие заказа. Проверяется код ответа и сообщение об ошибке')
    def test_accept_order_for_courier_with_incorrect_order_id(self):
        id_courier = create_courier_and_return_id()
        id_order = f'{create_order_and_return_id()}1'
        payload = {"id": id_order,
                   "courierId": id_courier}
        response = requests.put(f'{Urls.samokat_page}/api/v1/orders/accept/{id_order}?courierId={id_courier}',
                                      data=payload)
        assert response.status_code == 404 and 'Заказа с таким id не существует' in response.json()['message']

    @allure.title('Проверка отсутствия принятия заказа для курьера при некорректном id курьера')
    @allure.description(
        'Используются методы создания курьера и заказа и получения их id. Полученный id заказа и измененный id курьера отправляются в запрос на принятие заказа. Проверяется код ответа и сообщение об ошибке')
    def test_accept_order_for_courier_with_incorrect_courier_id(self):
        id_courier = f'{create_courier_and_return_id()}1'
        id_order = create_order_and_return_id()
        payload = {"id": id_order,
                   "courierId": id_courier}
        response = requests.put(f'{Urls.samokat_page}/api/v1/orders/accept/{id_order}?courierId={id_courier}',
                                      data=payload)
        assert response.status_code == 404 and 'Курьера с таким id не существует' in response.json()['message']

    @allure.title('Проверка отсутствия принятия заказа для курьера при незаполненном id курьера или id заказа')
    @allure.description('Используются методы создания курьера и заказа и получения их id. В запрос на принятие заказа отправляются неполные данные - только id курьера, только id заказа, пустые оба id. Проверяется код ответа и сообщение об ошибке')
    @pytest.mark.parametrize('courier, order', [['', create_order_and_return_id()], [create_courier_and_return_id(), ''], ['', '']])
    def test_accept_order_for_courier_without_courier_or_order(self, courier, order):
        id_courier = courier
        id_order = order
        payload = {"id": id_order,
                   "courierId": id_courier}
        response = requests.put(f'{Urls.samokat_page}/api/v1/orders/accept/{id_order}?courierId={id_courier}', data=payload)
        assert response.status_code == 400 and 'Недостаточно данных для поиска' in response.json()['message'] #тест падает по причине несоответствия кода и текста ошибки ожидаемым согласно требованиям, в случаях, когда не заполнен id заказа
