import time
import allure
import requests
from faker import Faker
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from global_constants.constants import DOMAIN_1, DOMAIN_2, DOMAIN_3, WRONG_DOMAIN, WRONG_CPU
from global_constants.constants import URL_FOR_API_REQUEST, URL_FOR_POST_REQUEST, length_of_password


class ProfilePage(BasePage):
    ADD_SERVER_LOCATOR = '//*[@data-bs-target="#addServerModal"]'
    DOMAIN_FIELD = '//*[@id="info_url"]'
    COUNT_OF_SERVERS = 'div.col-4.d-flex.flex-column.p-3'
    RAM_4_CONFIGURATION = '//*[@id="ram4"]'
    RAM_8_CONFIGURATION = '//*[@id="ram8"]'
    RAM_16_CONFIGURATION = '//*[@id="ram16"]'
    DELETE_SERVER_LOCATOR = '.btn.del-server-btn.btn-outline-danger'
    CPU_FIELD = '//*[@id="cpu"]'
    CLOSE_BUTTON_LOCATOR = '//*[@data-bs-dismiss="modal"]'

    def __init__(self, open_browser):
        super().__init__(open_browser)
        self.fake = Faker()
        self.random_credentials = self.generate_random_credentials(1)
        self.first_pair_credential = self.random_credentials[0]
        self.first_email, self.first_password = self.first_pair_credential
        self.register_users(self.random_credentials)

    def submit_and_check_alert(self, open_browser):
        submit_button = open_browser.find_element(By.XPATH, self.SUBMIT_LOCATOR)
        submit_button.click()
        alert_message = open_browser.find_element(By.XPATH, self.ALERT_MESSAGE)
        alert_message_text = alert_message.text
        assert alert_message_text == 'Input payload validation failed', f"Сообщение {alert_message_text} не найдено на странице."
        close_button = open_browser.find_element(By.XPATH, self.CLOSE_BUTTON_LOCATOR)
        close_button.click()
        self._wait(2)

    def fill_domain(self, open_browser, domain):
        domain_field = open_browser.find_element(By.XPATH, self.DOMAIN_FIELD)
        domain_field.clear()
        domain_field.send_keys(domain)

    def click_add_server_button(self, open_browser):
        add_server_button = WebDriverWait(open_browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, self.ADD_SERVER_LOCATOR))
        )
        add_server_button.click()

    def generate_random_credentials(self, num):
        credentials = []
        for _ in range(num):
            email = self.fake.email()
            password = self.fake.password(length=length_of_password, special_chars=True, digits=True, upper_case=True, lower_case=True)
            credentials.append((email, password))
        return credentials

    def register_users(self, credentials):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        for email, password in credentials:
            payload = {'email': email, 'password': password}
            response = requests.post(URL_FOR_POST_REQUEST, data=payload, headers=headers)
            if response.status_code == 201:
                print(f"Успешно зарегестрирован {email}")
            else:
                print(f"Произошла ошибка при регистрации {email}: {response.status_code} - {response.text}")

    def _find_and_click(self, by, value):
        element = self.browser.find_element(by, value)
        element.click()

    def _find_and_send_keys(self, by, value, keys):
        element = self.browser.find_element(by, value)
        element.clear()
        element.send_keys(keys)

    def _get_elements_count(self, by, value):
        elements = self.browser.find_elements(by, value)
        return len(elements)

    def _wait(self, seconds):
        time.sleep(seconds)

    def login(self, email, password):
        self._find_and_click(By.LINK_TEXT, self.SIGN_IN_LOCATOR)
        self._find_and_send_keys(By.XPATH, self.EMAIL_FIELD, email)
        self._find_and_send_keys(By.XPATH, self.PASSWORD_FIELD, password)
        self._find_and_click(By.XPATH, self.SUBMIT_LOCATOR)
        self._wait(1)

    def add_server(self, ram_id, domain):
        self._find_and_click(By.XPATH, self.ADD_SERVER_LOCATOR)
        self._wait(1)
        self._find_and_click(By.XPATH, ram_id)
        self._wait(1)
        self._find_and_send_keys(By.XPATH, self.DOMAIN_FIELD, domain)
        self._wait(1)
        self._find_and_click(By.XPATH, self.SUBMIT_LOCATOR)
        self._wait(1)
        count = self._get_elements_count(By.CSS_SELECTOR, self.COUNT_OF_SERVERS)
        print(f'Количество элементов: {count}')

    @allure.feature('Создать 3 сервера, проверить количество серверов на странице')
    def check_profile_server_page(self, open_browser):
        with allure.step('Авторизоваться'):
            self.login(self.first_email, self.first_password)
        with allure.step('Создать три сервера'):
            self.add_server(self.RAM_4_CONFIGURATION, DOMAIN_1)
            self.add_server(self.RAM_8_CONFIGURATION, DOMAIN_2)
            self.add_server(self.RAM_16_CONFIGURATION, DOMAIN_3)

            access_token = None
            cookies = open_browser.get_cookies()
            for cookie in cookies:
                if cookie['name'] == 'access_token':
                    access_token = cookie['value']
                    break

            headers = {
                'Authorization': f'Bearer {access_token}'
            }

            response = requests.get(URL_FOR_API_REQUEST, headers=headers)
            if response.status_code == 200:
                data = response.json()
                total_items = data.get('total_items')
                print(f'Total items: {total_items}')
            else:
                print(f'Ошибка запроса: {response.status_code}')
        with allure.step('Выйти из личного кабинета'):
            self.log_out(open_browser)

    @allure.feature('Удалить 1 сервер, проверить количество серверов на странице')
    def delete_server_page(self, open_browser):
        with allure.step('Авторизоваться'):
            self.login(self.first_email, self.first_password)
        with allure.step('Нажать на кнопку "Добавить сервер"'):
            self.click_add_server_button(open_browser)
        with allure.step('Заполнить форму'):
            ram_radiobutton = open_browser.find_element(By.XPATH, self.RAM_4_CONFIGURATION)
            ram_radiobutton.click()
            self._wait(1)
            self.fill_domain(open_browser, DOMAIN_1)
            self._wait(1)
            submit_button = open_browser.find_element(By.XPATH, self.SUBMIT_LOCATOR)
            submit_button.click()
            self._wait(1)
        with allure.step('Удалить сервер'):
            delete_button = open_browser.find_element(By.CSS_SELECTOR, self.DELETE_SERVER_LOCATOR)
            delete_button.click()
            alert = Alert(open_browser)
            alert.accept()

            access_token = None
            cookies = open_browser.get_cookies()
            for cookie in cookies:
                if cookie['name'] == 'access_token':
                    access_token = cookie['value']
                    break
            print(f"cookies[‘access_token’]: {access_token}")

            headers = {
                'Authorization': f'Bearer {access_token}'
            }

            response = requests.get(URL_FOR_API_REQUEST, headers=headers)
            if response.status_code == 200:
                data = response.json()
                total_items = data.get('total_items')

                print(f'Total items: {total_items}')
            else:
                print(f'Ошибка запроса: {response.status_code}')
        with allure.step('Выйти из личного кабинета'):
            self.log_out(open_browser)

    @allure.feature('Создать сервер где cpu равно не числу, а строке, например “XEON')
    def create_server_with_cpu(self, open_browser):
        with allure.step('Авторизоваться'):
            self.login(self.first_email, self.first_password)
        with allure.step('Нажать на кнопку "Добавить сервер"'):
            self.click_add_server_button(open_browser)
        with allure.step('Заполнить форму'):
            cpu_field = open_browser.find_element(By.XPATH, self.CPU_FIELD)
            cpu_field.clear()
            self._wait(1)
            cpu_field.send_keys(WRONG_CPU)
            self._wait(1)
            self.fill_domain(open_browser, DOMAIN_1)
            self._wait(1)
        with allure.step('Проверить валидационное сообщение'):
            self.submit_and_check_alert(open_browser)
            self._wait(1)
        with allure.step('Выйти из личного кабинета'):
            self.log_out(open_browser)

    @allure.feature('Создать сервер с некорректным доменом')
    def create_server_with_domain(self, open_browser):
        with allure.step('Авторизоваться'):
            self.login(self.first_email, self.first_password)
        with allure.step('Нажать на кнопку "Добавить сервер"'):
            self.click_add_server_button(open_browser)
        with allure.step('Заполнить форму'):
            self.fill_domain(open_browser, WRONG_DOMAIN)
            self._wait(1)
        with allure.step('Проверить валидационное сообщение'):
            self.submit_and_check_alert(open_browser)
            self._wait(1)
        with allure.step('Выйти из личного кабинета'):
            self.log_out(open_browser)



















