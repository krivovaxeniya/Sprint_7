import pytest
from create_data import *
import random
import json
import allure


class TestCreateCourier:

    @allure.title('Проверка успешного создания нового курьера')
    @allure.description('Отправляется запрос на регистрацию курьера с данными, которые ранее не использовались. Проверяется код ответа и сообщение об успешном выполнении запроса')
    def test_create_one_courier(self):
        payload = {"login": f'slowpoke{random.randint(0, 100)}',
                   "password": '12345678',
                   "firstName": 'Ivan'}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert response.status_code == 201 and response.text == '{"ok":true}'

    @allure.title('Проверка отсутствия регистрации при повторном создании курьера')
    @allure.description(
        'Используется метод регистрации нового курьера, после чего данные регистрации используются повторно в запросе на регистрацию. Проверяется код ответа и сообщение об ошибке')
    def test_create_one_courier_twice(self):
        user_data = register_new_courier_and_return_login_password()
        payload = {"login": user_data[0],
                   "password": user_data[1],
                   "firstName": user_data[2]}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert response.status_code == 409 and response.json()['message'] == 'Этот логин уже используется' #тест падает по причине того, что сообщение об ошибке отличается от указанного в требованиях

    @allure.title('Проверка отсутствия регистрации при попытке регистрации с незаполненным обязательным параметром')
    @allure.description('Отправляется запрос на регистрацию курьера при незаполненном одном из обязательных параметров - логине или пароле. Проверяется код ответа и сообщение об ошибке')
    @pytest.mark.parametrize('login, password', [['master', ''], ['', '12345']])
    def test_create_courier_without_login_or_password(self, login, password):
        payload = {"login": login,
                   "password": password,
                   "firstName": 'Ivan'}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для создания учетной записи'

    @allure.title('Проверка успешной регистрации курьера при незаполненном имени')
    @allure.description(
        'Отправляется запрос на регистрацию курьера при незаполненном имени. Проверяется код ответа и сообщение об успешной регистрации')
    def test_create_courier_without_first_name(self):
        payload = {"login": f'slowpoke{random.randint(0, 100)}',
                   "password": '12345678',
                   "firstName": ''}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        assert response.status_code == 201 and response.text == '{"ok":true}'


class TestLoginCourier:

    @allure.title('Проверка успешной авторизации зарегистрированного курьера')
    @allure.description(
        'Используется метод регистрации нового курьера, после чего данные регистрации используются в запросе на авторизацию. Проверяется код ответа и наличие id в ответе')
    def test_authorization_courier(self):
        user_data = register_new_courier_and_return_login_password()
        payload = {"login": user_data[0],
                   "password": user_data[1]}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        assert response.status_code == 200 and 'id' in response.text

    @allure.title('Проверка отсутствия авторизации курьера с некорректным паролем')
    @allure.description(
        'Используется метод регистрации нового курьера, после чего в запросе на авторизацию указывается логин и не соответствующий ему пароль. Проверяется код ответа и сообщение об ошибке')
    def test_authorization_courier_with_incorrect_password(self):
        user_data = register_new_courier_and_return_login_password()
        payload = {"login": user_data[0],
                   "password": f'{user_data[1]}1'}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        assert response.status_code == 404 and response.json()['message'] == 'Учетная запись не найдена'

    @allure.title('Проверка отсутствия авторизации курьера с некорректным логином')
    @allure.description(
        'Используется метод регистрации нового курьера, после чего в запросе на авторизацию указывается пароль и не соответствующий ему логин. Проверяется код ответа и сообщение об ошибке')
    def test_authorization_courier_with_incorrect_login(self):
        user_data = register_new_courier_and_return_login_password()
        payload = {"login": f'{user_data[0]}1',
                   "password": user_data[1]}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        assert response.status_code == 404 and response.json()['message'] == 'Учетная запись не найдена'

    @allure.title('Проверка отсутствия авторизации при попытке авторизации с незаполненным обязательным параметром')
    @allure.description('Отправляется запрос на авторизацию курьера при незаполненных обязательных параметрах - логине или пароле или логине и пароле. Проверяется код ответа и сообщение об ошибке')
    @pytest.mark.parametrize('login, password', [[register_new_courier_and_return_login_password()[0], ''], ['', register_new_courier_and_return_login_password()[1]]])
    def test_authorization_without_login_or_password(self, login, password):
        payload = {"login": login,
                   "password": password}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для входа'


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
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/orders', data=payload_string)
        assert response.status_code == 201 and 'track' in response.text


class TestGetOrderList:

    @allure.title('Проверка успешного получения списка заказов')
    @allure.description('Отправляется запрос на получение списка заказов. Проверяется код ответа, наличие orders в ответе и список всех ключей в теле ответа')
    def test_get_order_list(self):
        response = requests.get('https://qa-scooter.praktikum-services.ru/api/v1/orders')
        order_keys = ['id', 'courierId', 'firstName', 'lastName', 'address', 'metroStation', 'phone', 'rentTime', 'deliveryDate', 'track', 'color', 'comment', 'createdAt', 'updatedAt', 'status']
        assert response.status_code == 200 and 'orders' in response.json() and list(response.json()["orders"][0].keys()) == order_keys


class TestDeleteCourier:

    @allure.title('Проверка успешного удаления курьера')
    @allure.description('Используется метод регистрации курьера и получения его id. Отправляется запрос на удаление курьера с выбранным id. Проверяется код ответа и сообщение об успешном выполнении запроса')
    def test_delete_courier(self):
        id_courier = create_courier_and_return_id()
        payload_del = {"id": id_courier}
        response_del = requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{id_courier}', data = payload_del)
        assert response_del.status_code == 200 and response_del.text == '{"ok":true}'

    @allure.title('Проверка отсутствия удаления курьера при незаполненном id')
    @allure.description('Отправляется запрос на удаление курьера с незаполненным id. Проверяется код ответа и сообщение об ошибке')
    def test_delete_courier_without_id(self):
        id_courier = ""
        payload_del = {"id": id_courier}
        response_del = requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{id_courier}',
                                       data=payload_del)
        assert response_del.status_code == 400 and response_del.json()['message'] == 'Недостаточно данных для удаления курьера' #тест падает по причине несоответствия кода и текста ошибки ожидаемым согласно требованиям

    @allure.title('Проверка отсутствия удаления курьера с несуществующим id')
    @allure.description(
        'Используется метод регистрации курьера и получения его id. Отправляется запрос на удаление курьера с id, отличным от полученного. Проверяется код ответа и сообщение об ошибке')
    def test_delete_courier_with_not_exist_id(self):
        id_courier = f'{create_courier_and_return_id()}1'
        payload_del = {"id": id_courier}
        response_del = requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{id_courier}',
                                       data=payload_del)
        assert response_del.status_code == 404 and 'Курьера с таким id нет' in response_del.json()['message']


class TestAcceptOrder:

    @allure.title('Проверка успешного принятия заказа для курьера')
    @allure.description('Используются методы создания курьера и заказа и получения их id. Полученные данные отправляются в запрос на принятие заказа. Проверяется код ответа и сообщение об успешном выполнении запроса')
    def test_accept_order_for_courier(self):
        id_courier = create_courier_and_return_id()
        id_order = create_order_and_return_id()
        payload = {"id": id_order,
                   "courierId": id_courier}
        response = requests.put(f'https://qa-scooter.praktikum-services.ru/api/v1/orders/accept/{id_order}?courierId={id_courier}',
                                      data=payload)
        assert response.status_code == 200 and response.text == '{"ok":true}'

    @allure.title('Проверка отсутствия принятия заказа для курьера при некорректном id заказа')
    @allure.description('Используются методы создания курьера и заказа и получения их id. Полученный id курьера и измененный id заказа отправляются в запрос на принятие заказа. Проверяется код ответа и сообщение об ошибке')
    def test_accept_order_for_courier_with_incorrect_order_id(self):
        id_courier = create_courier_and_return_id()
        id_order = f'{create_order_and_return_id()}1'
        payload = {"id": id_order,
                   "courierId": id_courier}
        response = requests.put(f'https://qa-scooter.praktikum-services.ru/api/v1/orders/accept/{id_order}?courierId={id_courier}',
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
        response = requests.put(f'https://qa-scooter.praktikum-services.ru/api/v1/orders/accept/{id_order}?courierId={id_courier}',
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
        response = requests.put(f'https://qa-scooter.praktikum-services.ru/api/v1/orders/accept/{id_order}?courierId={id_courier}', data=payload)
        assert response.status_code == 400 and 'Недостаточно данных для поиска' in response.json()['message'] #тест падает по причине несоответствия кода и текста ошибки ожидаемым согласно требованиям, в случаях, когда не заполнен id заказа


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
        response_order = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/orders', data=payload_string)
        track_order = response_order.json()['track']
        payload = {"t": track_order}
        response = requests.get(f'https://qa-scooter.praktikum-services.ru/api/v1/orders/track?t={track_order}', data=payload)
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
        response_order = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/orders', data=payload_string)
        track_order = f'{response_order.json()["track"]}1'
        payload = {"t": track_order}
        response = requests.get(f'https://qa-scooter.praktikum-services.ru/api/v1/orders/track?t={track_order}', data=payload)
        assert response.status_code == 404 and 'Заказ не найден' in response.json()['message']

    @allure.title('Проверка отсутствия получения заказа при незаполненном номере')
    @allure.description('Отправляется запрос для получения информации по заказу с незаполненным номером. Проверяется код ответа и сообщение об ошибке')
    def test_get_order_without_track(self):
        track_order = ""
        payload = {"t": track_order}
        response = requests.get(f'https://qa-scooter.praktikum-services.ru/api/v1/orders/track?t={track_order}',
                                data=payload)
        assert response.status_code == 400 and 'Недостаточно данных для поиска' in response.json()['message']
