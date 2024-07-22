import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class RegistrationPage(BasePage):
    SIGN_UP_LOCATOR = "Signup"

    def __init__(self, open_browser):
        super().__init__(open_browser)

    def sign_up(self, open_browser):
        sign_up_button = open_browser.find_element(By.LINK_TEXT, self.SIGN_UP_LOCATOR)
        sign_up_button.click()

    @allure.feature('Проверить, что страница Регистрация пользователя открывается')
    def check_correct_registration_open_page(self, open_browser):
        with allure.step('Авторизоваться'):
            sign_up_button = open_browser.find_element(By.LINK_TEXT, self.SIGN_UP_LOCATOR)
            sign_up_button.click()
        with allure.step('Проверить, что текст "Регистрация пользователя" есть на странице'):
            page_name = open_browser.find_element(By.CSS_SELECTOR, "h1")
            page_name_text = page_name.text
            assert page_name_text == 'Регистрация пользователя', f"Сообщение {page_name_text} не найдено на странице"

    @allure.feature('Проверить регистрацию по парам: имя/пароль, email/пустой пароль, некорректный email/пароль')
    def check_registration_page_with_invalid_data(self, open_browser, email, password):
        with allure.step('Авторизоваться'):
            self.sign_up(open_browser)
            self.fill_registration_form(open_browser, email, password)
            self.submit_registration_form(open_browser)
        with allure.step('Проверить валидационное сообщение'):
            alert_message = open_browser.find_element(By.XPATH, self.ALERT_MESSAGE)
            alert_message_text = alert_message.text
            assert alert_message_text == 'Input payload validation failed', f"Сообщение {alert_message_text} не найдено на странице."
            open_browser.refresh()

    @allure.feature('Проверка страницы регистрации с валидными данными')
    def check_registration_page_with_valid_data(self, open_browser, email, password):
        with allure.step('Авторизоваться'):
            self.sign_up(open_browser)
            self.fill_registration_form(open_browser, email, password)
            self.submit_registration_form(open_browser)
        with allure.step('Проверить, что личный кабинет открылся'):
            log_out_button = open_browser.find_element(By.XPATH, self.LOG_OUT_LOCATOR)
            assert log_out_button is not None, "Кнопка 'Logout' не найдена на странице."

    @allure.feature('Проверка страницы регистрации с уже использованными данными')
    def check_registration_page_with_used_data(self, open_browser, email, password):
        with allure.step('Авторизоваться'):
            self.log_out(open_browser)
            self.sign_up(open_browser)
            self.fill_registration_form(open_browser, email, password)
            self.submit_registration_form(open_browser)
        with allure.step('Проверить валидационное сообщение'):
            alert_message = open_browser.find_element(By.XPATH, self.ALERT_MESSAGE)
            assert alert_message is not None, "Сообщение об ошибке не появилось"







