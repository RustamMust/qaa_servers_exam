import pytest
from pages.authorization_page import AuthorizationPage
from pages.main_servers_page import ServersPage
from pages.profile_page import ProfilePage
from pages.registration_page import RegistrationPage
from pages.base_page import first_pair_credential
from global_constants.constants import name_instead_of_email, valid_password, valid_email, empty_password
from global_constants.constants import invalid_email, non_registered_email


@pytest.mark.xfail(reason="Ошибка в карточке с городом Нью Йорк. 12 CPU, 24 RAM, 256 SSD цена должна быть 256")
def test_server_page(open_browser):
    """Проверить корректность расчета стоимости серверов. Формула расчета price = cpu**2 + ram*2 + ssd/4"""
    server = ServersPage(open_browser)
    server.check_server_price(open_browser)


def test_correct_registration_open_page(open_browser):
    """Проверить, что страница Регистрация пользователя открывается"""
    server = RegistrationPage(open_browser)
    server.check_correct_registration_open_page(open_browser)


@pytest.mark.parametrize("email, password", [
    (name_instead_of_email, valid_password),
    (valid_email, empty_password),
    (invalid_email, valid_password),
])
def test_registration_page_with_invalid_data(open_browser, email, password):
    """Проверить регистрацию по парам: имя/пароль, email/пустой пароль, некорректный email/пароль"""
    server = RegistrationPage(open_browser)
    if email == valid_email and password == empty_password:
        pytest.xfail("Пустое поле 'Пароль' не вызывает баннер 'Input payload validation failed'")
    server.check_registration_page_with_invalid_data(open_browser, email=email, password=password)


@pytest.mark.parametrize("email, password", [first_pair_credential])
def test_registration_page_with_valid_data(open_browser, email, password):
    """Проверить регистрацию по паре email/пароль"""
    server = RegistrationPage(open_browser)
    server.check_registration_page_with_valid_data(open_browser, email=email, password=password)


@pytest.mark.parametrize("email, password", [first_pair_credential])
def test_registration_page_with_used_data(open_browser, email, password):
    """Попробовать повторно зарегистрироваться с тем же значением email/пароль"""
    server = RegistrationPage(open_browser)
    server.check_registration_page_with_used_data(open_browser, email=email, password=password)


def test_correct_authorization_open_page(open_browser):
    """Проверить, что страница Авторизация пользователя открывается"""
    server = AuthorizationPage(open_browser)
    server.check_correct_authorization_open_page(open_browser)


@pytest.mark.parametrize("email, password", [
    (non_registered_email, valid_password)
])
def test_authorization_page_with_invalid_data(open_browser, email, password):
    """Попробовать авторизоваться с некорректной парой email/пароль"""
    server = AuthorizationPage(open_browser)
    server.check_authorization_page_with_invalid_data(open_browser, email=email, password=password)


@pytest.mark.parametrize("email, password", [first_pair_credential])
def test_authorization_page_with_valid_data(open_browser, email, password):
    """Авторизоваться с корректным значением email/пароль"""
    server = AuthorizationPage(open_browser)
    server.check_authorization_page_with_valid_data(open_browser, email=email, password=password)


@pytest.mark.parametrize("email, password", [first_pair_credential])
def test_compare_access_token(open_browser, email, password):
    """Сравнить значение cookies[‘access_token’] до и после успешной авторизации"""
    server = AuthorizationPage(open_browser)
    server.compare_access_token(open_browser, email=email, password=password)


def test_profile_server_page(open_browser):
    """Создать 3 сервера, проверить количество серверов на странице"""
    server = ProfilePage(open_browser)
    server.check_profile_server_page(open_browser)


def test_delete_server_page(open_browser):
    """Удалить 1 сервер, проверить количество серверов на странице"""
    server = ProfilePage(open_browser)
    server.delete_server_page(open_browser)


def test_create_server_with_cpu(open_browser):
    """Создать сервер где cpu равно не числу, а строке, например “XEON”"""
    server = ProfilePage(open_browser)
    server.create_server_with_cpu(open_browser)


def test_create_server_with_domain(open_browser):
    """Создать сервер с некорректным доменом"""
    server = ProfilePage(open_browser)
    server.create_server_with_domain(open_browser)














