import pytest
from create_data import *
import allure
from urls import Urls

class TestDeleteCourier:

    @allure.title('Проверка успешного удаления курьера')
    @allure.description('Используется метод регистрации курьера и получения его id. Отправляется запрос на удаление курьера с выбранным id. Проверяется код ответа и сообщение об успешном выполнении запроса')
    def test_delete_courier(self):
        id_courier = create_courier_and_return_id()
        payload_del = {"id": id_courier}
        response_del = requests.delete(f'{Urls.samokat_page}/api/v1/courier/{id_courier}', data = payload_del)
        assert response_del.status_code == 200 and response_del.text == '{"ok":true}'

    @allure.title('Проверка отсутствия удаления курьера при незаполненном id')
    @allure.description('Отправляется запрос на удаление курьера с незаполненным id. Проверяется код ответа и сообщение об ошибке')
    def test_delete_courier_without_id(self):
        id_courier = ""
        payload_del = {"id": id_courier}
        response_del = requests.delete(f'{Urls.samokat_page}/api/v1/courier/{id_courier}',
                                       data=payload_del)
        assert response_del.status_code == 400 and response_del.json()['message'] == 'Недостаточно данных для удаления курьера' #тест падает по причине несоответствия кода и текста ошибки ожидаемым согласно требованиям

    @allure.title('Проверка отсутствия удаления курьера с несуществующим id')
    @allure.description(
        'Используется метод регистрации курьера и получения его id. Отправляется запрос на удаление курьера с id, отличным от полученного. Проверяется код ответа и сообщение об ошибке')
    def test_delete_courier_with_not_exist_id(self):
        id_courier = f'{create_courier_and_return_id()}1'
        payload_del = {"id": id_courier}
        response_del = requests.delete(f'{Urls.samokat_page}/api/v1/courier/{id_courier}',
                                       data=payload_del)
        assert response_del.status_code == 404 and 'Курьера с таким id нет' in response_del.json()['message']
