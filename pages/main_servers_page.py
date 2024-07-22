import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import re
from global_constants.constants import cpu_number, ram_number, ssd_number


class ServersPage(BasePage):
    CARDS_LOCATOR = "card"
    CARD_TEXT_LOCATOR = "card-text"
    PRICE_TEXT_LOCATOR = ".btn.btn-primary"

    def __init__(self, open_browser):
        super().__init__(open_browser)

    def extract_number(self, text):
        match = re.search(r'\d+', text)
        return int(match.group()) if match else 0

    def get_card_details(self, card):
        card_text = card.find_element(By.CLASS_NAME, self.CARD_TEXT_LOCATOR).text
        lines = card_text.split('\n')

        cpu = self.extract_number([line for line in lines if "CPU" in line][0])
        ram = self.extract_number([line for line in lines if "RAM" in line][0])
        ssd = self.extract_number([line for line in lines if "SSD" in line][0])
        city = lines[-1]

        price_text = card.find_element(By.CSS_SELECTOR, self.PRICE_TEXT_LOCATOR).text
        price = self.extract_number(price_text)

        return cpu, ram, ssd, city, price

    def calculate_expected_price(self, cpu, ram, ssd):
        return (cpu ** cpu_number) + (ram * ram_number) + (ssd / ssd_number)

    @allure.feature('Проверить корректность расчета стоимости серверов')
    def check_server_price(self, open_browser):
        cards = open_browser.find_elements(By.CLASS_NAME, self.CARDS_LOCATOR)

        for card in cards:
            cpu, ram, ssd, city, price = self.get_card_details(card)
            expected_price = self.calculate_expected_price(cpu, ram, ssd)

            assert price == expected_price, (
                f"Ошибка в карточке с городом {city}! Для {cpu} CPU, {ram} RAM и {ssd} SSD "
                f"цена {price} не совпадает с ожидаемой {expected_price}."
            )











