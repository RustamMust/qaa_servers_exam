import time
import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AuthorizationPage(BasePage):

    def __init__(self, open_browser):
        super().__init__(open_browser)

    def sign_in(self, open_browser):
        sign_in_button = open_browser.find_element(By.LINK_TEXT, self.SIGN_IN_LOCATOR)
        sign_in_button.click()

    @allure.feature('Проверить, что страница Авторизация пользователя открывается')
    def check_correct_authorization_open_page(self, open_browser):
        with allure.step('Авторизоваться'):
            self.sign_in(open_browser)
        with allure.step('Проверить, что текст "Авторизация пользователя" есть на странице'):
            page_name = open_browser.find_element(By.CSS_SELECTOR, "h1")
            page_name_text = page_name.text
            assert page_name_text == 'Авторизация пользователя', f"Сообщение {page_name_text} не найдено на странице"

    @allure.feature('Попробовать авторизоваться с некорректной парой email/пароль')
    def check_authorization_page_with_invalid_data(self, open_browser, email, password):
        with allure.step('Авторизоваться'):
            self.sign_in(open_browser)
        with allure.step('Заполнить поля некорректной парой email/пароль'):
            self.fill_registration_form(open_browser, email, password)
            self.submit_registration_form(open_browser)
        with allure.step('Проверить валидационное сообщение'):
            alert_message = open_browser.find_element(By.XPATH, self.ALERT_MESSAGE)
            alert_message_text = alert_message.text
            assert alert_message_text == 'email or password does not match', f"Сообщение {alert_message_text} не найдено на странице."

    @allure.feature('Авторизоваться с корректным значением email/пароль')
    def check_authorization_page_with_valid_data(self, open_browser, email, password):
        with allure.step('Авторизоваться'):
            self.sign_in(open_browser)
        with allure.step('Заполнить поля корректным значением email/пароль'):
            self.fill_registration_form(open_browser, email, password)
            self.submit_registration_form(open_browser)
        with allure.step('Проверить, что личный кабинет открылся'):
            log_out_button = open_browser.find_element(By.XPATH, self.LOG_OUT_LOCATOR)
            assert log_out_button is not None, "Кнопка 'Logout' не найдена на странице."

    @allure.feature('Сравнить значение cookies[‘access_token’] до и после успешной авторизации')
    def compare_access_token(self, open_browser, email, password):
        with allure.step('Разлогиниться'):
            self.log_out(open_browser)
        with allure.step('Заполнить форму авторизации'):
            self.fill_registration_form(open_browser, email, password)

        with allure.step('Получение значения cookies["access_token"] до авторизации'):
            initial_access_token = None
            cookies = open_browser.get_cookies()
            for cookie in cookies:
                if cookie['name'] == 'access_token':
                    initial_access_token = cookie['value']
                    break

        with allure.step('Нажать кнопку для входа в личный кабинет'):
            self.submit_registration_form(open_browser)
            time.sleep(2)

        with allure.step('Получение значения cookies["access_token"] после авторизации'):
            post_login_access_token = None
            cookies = open_browser.get_cookies()
            for cookie in cookies:
                if cookie['name'] == 'access_token':
                    post_login_access_token = cookie['value']
                    break

        with allure.step('Сравнение значений cookies["access_token"]'):
            assert initial_access_token != post_login_access_token, "Access token не изменился после авторизации"
            self.log_out(open_browser)








