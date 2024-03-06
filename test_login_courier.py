import pytest
from create_data import *
import allure
from urls import Urls


class TestLoginCourier:

    @allure.title('Проверка успешной авторизации зарегистрированного курьера')
    @allure.description(
        'Используется метод регистрации нового курьера, после чего данные регистрации используются в запросе на авторизацию. Проверяется код ответа и наличие id в ответе')
    def test_authorization_courier(self):
        user_data = register_new_courier_and_return_login_password()
        payload = {"login": user_data[0],
                   "password": user_data[1]}
        response = requests.post(f'{Urls.samokat_page}/api/v1/courier/login', data=payload)
        assert response.status_code == 200 and 'id' in response.text

    @allure.title('Проверка отсутствия авторизации курьера с некорректным паролем')
    @allure.description(
        'Используется метод регистрации нового курьера, после чего в запросе на авторизацию указывается логин и не соответствующий ему пароль. Проверяется код ответа и сообщение об ошибке')
    def test_authorization_courier_with_incorrect_password(self):
        user_data = register_new_courier_and_return_login_password()
        payload = {"login": user_data[0],
                   "password": f'{user_data[1]}1'}
        response = requests.post(f'{Urls.samokat_page}/api/v1/courier/login', data=payload)
        assert response.status_code == 404 and response.json()['message'] == 'Учетная запись не найдена'

    @allure.title('Проверка отсутствия авторизации курьера с некорректным логином')
    @allure.description(
        'Используется метод регистрации нового курьера, после чего в запросе на авторизацию указывается пароль и не соответствующий ему логин. Проверяется код ответа и сообщение об ошибке')
    def test_authorization_courier_with_incorrect_login(self):
        user_data = register_new_courier_and_return_login_password()
        payload = {"login": f'{user_data[0]}1',
                   "password": user_data[1]}
        response = requests.post(f'{Urls.samokat_page}/api/v1/courier/login', data=payload)
        assert response.status_code == 404 and response.json()['message'] == 'Учетная запись не найдена'

    @allure.title('Проверка отсутствия авторизации при попытке авторизации с незаполненным обязательным параметром')
    @allure.description('Отправляется запрос на авторизацию курьера при незаполненных обязательных параметрах - логине или пароле или логине и пароле. Проверяется код ответа и сообщение об ошибке')
    @pytest.mark.parametrize('login, password', [[register_new_courier_and_return_login_password()[0], ''], ['', register_new_courier_and_return_login_password()[1]]])
    def test_authorization_without_login_or_password(self, login, password):
        payload = {"login": login,
                   "password": password}
        response = requests.post(f'{Urls.samokat_page}/api/v1/courier/login', data=payload)
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для входа'
