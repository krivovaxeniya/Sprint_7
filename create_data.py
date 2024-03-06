import requests
import random
import string
import json
import allure




@allure.step('Используется метод регистрации нового курьера, который возвращает список из логина и пароля')
def register_new_courier_and_return_login_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login_pass = []
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)
    return login_pass


@allure.step('Используется метод создания нового заказа, который возвращает id заказа')
def create_order_and_return_id():
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
    response_get_order = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/orders', data=payload_string)
    track_order = response_get_order.json()['track']
    payload_track = {"t": track_order}
    response_order = requests.get(f'https://qa-scooter.praktikum-services.ru/api/v1/orders/track?t={track_order}',
                                  data=payload_track)
    id_order = response_order.json()["order"]["id"]
    return id_order


@allure.step('Используется метод для возврата id курьера, использует метод создания курьера')
def create_courier_and_return_id():
    user_data = register_new_courier_and_return_login_password()
    payload_auth = {"login": user_data[0],
                    "password": user_data[1]}
    response_auth = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload_auth)
    id_courier = response_auth.json()['id']
    return id_courier
