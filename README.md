# Sprint_7
<h3>Автотесты, реализованные для сервиса Яндекс.Самокат</h3>

<h4>test_yandex_samokat.TestCreateCourier - тесты для проверки создания курьера</h4>
Проверка эндпоинта /api/v1/courier</br>
Метод запроса <b>POST</b>
<table>
  <thead>
  </thead>
  <tbody>
    <tr>
      <td>test_create_one_courier</td>
      <td>Проверка успешного создания нового курьера</td>
    </tr>
    <tr>
      <td>test_create_one_courier_twice</td>
      <td>Проверка отсутствия регистрации при повторном создании курьера</td>
    </tr>
    <tr>
      <td>test_create_courier_without_login_or_password</td>
      <td>Проверка отсутствия регистрации при попытке регистрации с незаполненным обязательным параметром</td>
    </tr>
    <tr>
      <td>test_create_courier_without_first_name</td>
      <td>Проверка успешной регистрации курьера при незаполненном имени</td>
    </tr>
  </tbody>
</table>

<h4>test_yandex_samokat.TestLoginCourier - тесты для проверки авторизации курьера</h4>
Проверка эндпоинта /api/v1/courier/login</br>
Метод запроса <b>POST</b>
<table>
  <thead>
  </thead>
  <tbody>
    <tr>
      <td>test_authorization_courier</td>
      <td>Проверка успешной авторизации зарегистрированного курьера</td>
    </tr>
    <tr>
      <td>test_authorization_courier_with_incorrect_password</td>
      <td>Проверка отсутствия авторизации курьера с некорректным паролем</td>
    </tr>
    <tr>
      <td>test_authorization_courier_with_incorrect_login</td>
      <td>Проверка отсутствия авторизации курьера с некорректным логином</td>
    </tr>
    <tr>
      <td>test_authorization_without_login_or_password</td>
      <td>Проверка отсутствия авторизации при попытке авторизации с незаполненным обязательным параметром</td>
    </tr>
  </tbody>
</table>

<h4>test_yandex_samokat.TestCreateOrder - тесты для проверки создания заказа</h4>
Проверка эндпоинта /api/v1/orders</br>
Метод запроса <b>POST</b>
<table>
  <thead>
  </thead>
  <tbody>
    <tr>
      <td>test_create_order</td>
      <td>Проверка успешного создания заказа с различным значением параметра цвет</td>
    </tr>
  </tbody>
</table>

<h4>test_yandex_samokat.TestGetOrderList - тесты для проверки получения списка заказов</h4>
Проверка эндпоинта /api/v1/orders</br>
Метод запроса <b>GET</b>
<table>
  <thead>
  </thead>
  <tbody>
    <tr>
      <td>test_get_order_list</td>
      <td>Проверка успешного получения списка заказов</td>
    </tr>
  </tbody>
</table>

<h4>test_yandex_samokat.TestDeleteCourier - тесты для проверки удаления курьера</h4>
Проверка эндпоинта /api/v1/courier/:id</br>
Метод запроса <b>DELETE</b>
<table>
  <thead>
  </thead>
  <tbody>
    <tr>
      <td>test_delete_courier</td>
      <td>Проверка успешного удаления курьера</td>
    </tr>
    <tr>
      <td>test_delete_courier_without_id</td>
      <td>Проверка отсутствия удаления курьера при незаполненном id</td>
    </tr>
    <tr>
      <td>test_delete_courier_with_not_exist_id</td>
      <td>Проверка отсутствия удаления курьера с несуществующим id</td>
    </tr>
  </tbody>
</table>

<h4>test_yandex_samokat.TestAcceptOrder - тесты для проверки принятия заказа</h4>
Проверка эндпоинта /v1/orders/accept/id:?courierId=value</br>
Метод запроса <b>PUT</b>
<table>
  <thead>
  </thead>
  <tbody>
    <tr>
      <td>test_accept_order_for_courier</td>
      <td>Проверка успешного принятия заказа для курьера</td>
    </tr>
    <tr>
      <td>test_accept_order_for_courier_with_incorrect_order_id</td>
      <td>Проверка отсутствия принятия заказа для курьера при некорректном id заказа</td>
    </tr>
    <tr>
      <td>test_accept_order_for_courier_with_incorrect_courier_id</td>
      <td>Проверка отсутствия принятия заказа для курьера при некорректном id курьера</td>
    </tr>
    <tr>
      <td>test_accept_order_for_courier_without_courier_or_order</td>
      <td>Проверка отсутствия принятия заказа для курьера при незаполненном id курьера или id заказа</td>
    </tr>
  </tbody>
</table>

<h4>test_yandex_samokat.TestGetOrderByTrack - тесты для проверки получения заказа по номеру</h4>
Проверка эндпоинта /api/v1/orders/track?t=value</br>
Метод запроса <b>GET</b>
<table>
  <thead>
  </thead>
  <tbody>
    <tr>
      <td>test_get_order_by_track</td>
      <td>Проверка успешного получения заказа по номеру</td>
    </tr>
    <tr>
      <td>test_get_order_with_incorrect_track</td>
      <td>Проверка отсутствия получения заказа при некорректном номере</td>
    </tr>
    <tr>
      <td>test_get_order_without_track</td>
      <td>Проверка отсутствия получения заказа при незаполненном номере</td>
    </tr>
  </tbody>
</table>

Для работы необходимы библиотеки: </br>
<li>pytest</li>
<li>json</li>
<li>random</li>
<li>allure</li>

Запуск тестов:  <b>pytest -v</b> </br>
Построение отчета о тестировании: <b>allure serve allure_results</b> 