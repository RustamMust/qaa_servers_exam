from faker import Faker
from selenium.webdriver.common.by import By
from global_constants.constants import number_of_credentials, length_of_password


def generate_random_credentials(num):
    fake = Faker()
    credentials = []
    for _ in range(num):
        email = fake.email()
        password = fake.password(length=length_of_password, special_chars=True, digits=True, upper_case=True, lower_case=True)
        credentials.append((email, password))
    return credentials


random_credentials = generate_random_credentials(number_of_credentials)
first_pair_credential = random_credentials[0]


class BasePage:
    SIGN_IN_LOCATOR = "Signin"
    EMAIL_FIELD = '//*[@id="email"]'
    PASSWORD_FIELD = '//*[@id="password"]'
    SUBMIT_LOCATOR = '//*[@type="submit"]'
    ALERT_MESSAGE = '//*[@class="alert alert-danger alert-dismissible"]'
    LOG_OUT_LOCATOR = '//*[@id="logout-btn"]'

    def __init__(self, browser):
        self.browser = browser

    def fill_registration_form(self, open_browser, email, password):
        email_field = open_browser.find_element(By.XPATH, self.EMAIL_FIELD)
        email_field.clear()
        email_field.send_keys(email)
        password_field = open_browser.find_element(By.XPATH, self.PASSWORD_FIELD)
        password_field.clear()
        password_field.send_keys(password)

    def submit_registration_form(self, open_browser):
        submit_button = open_browser.find_element(By.XPATH, self.SUBMIT_LOCATOR)
        submit_button.click()

    def log_out(self, open_browser):
        log_out_button = open_browser.find_element(By.XPATH, self.LOG_OUT_LOCATOR)
        log_out_button.click()





