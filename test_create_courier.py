import pytest
from create_data import *
import random
import allure
from urls import Urls


class TestCreateCourier:

    @allure.title('Проверка успешного создания нового курьера')
    @allure.description('Отправляется запрос на регистрацию курьера с данными, которые ранее не использовались. Проверяется код ответа и сообщение об успешном выполнении запроса')
    def test_create_one_courier(self):
        payload = {"login": f'slowpoke{random.randint(0, 1000)}',
                   "password": '12345678',
                   "firstName": 'Ivan'}
        response = requests.post(f'{Urls.samokat_page}/api/v1/courier', data=payload)
        assert response.status_code == 201 and response.text == '{"ok":true}'

    @allure.title('Проверка отсутствия регистрации при повторном создании курьера')
    @allure.description(
        'Используется метод регистрации нового курьера, после чего данные регистрации используются повторно в запросе на регистрацию. Проверяется код ответа и сообщение об ошибке')
    def test_create_one_courier_twice(self):
        user_data = register_new_courier_and_return_login_password()
        payload = {"login": user_data[0],
                   "password": user_data[1],
                   "firstName": user_data[2]}
        response = requests.post(f'{Urls.samokat_page}/api/v1/courier', data=payload)
        assert response.status_code == 409 and response.json()['message'] == 'Этот логин уже используется' #тест падает по причине того, что сообщение об ошибке отличается от указанного в требованиях

    @allure.title('Проверка отсутствия регистрации при попытке регистрации с незаполненным обязательным параметром')
    @allure.description('Отправляется запрос на регистрацию курьера при незаполненном одном из обязательных параметров - логине или пароле. Проверяется код ответа и сообщение об ошибке')
    @pytest.mark.parametrize('login, password', [['master', ''], ['', '12345']])
    def test_create_courier_without_login_or_password(self, login, password):
        payload = {"login": login,
                   "password": password,
                   "firstName": 'Ivan'}
        response = requests.post(f'{Urls.samokat_page}/api/v1/courier', data=payload)
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для создания учетной записи'

    @allure.title('Проверка успешной регистрации курьера при незаполненном имени')
    @allure.description(
        'Отправляется запрос на регистрацию курьера при незаполненном имени. Проверяется код ответа и сообщение об успешной регистрации')
    def test_create_courier_without_first_name(self):
        payload = {"login": f'slowpoke{random.randint(0, 1000)}',
                   "password": '12345678',
                   "firstName": ''}
        response = requests.post(f'{Urls.samokat_page}/api/v1/courier', data=payload)
        assert response.status_code == 201 and response.text == '{"ok":true}'
