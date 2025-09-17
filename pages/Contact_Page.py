from allure_commons.types import AttachmentType
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from utils.passenger_utils import calculate_age

AGE_RANGES = {
    "infant": (0, 1),
    "children": (2, 11),
    "tng": (12, 14),
    "adults": (15, 120)
}
MONTH_NAMES = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}
class ContactPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Initializing contacts page")
    def wait_for_contact_page(self):
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(@class, 'title-h1')]//span[contains(text(), 'Pasajeros')]")))
        self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[starts-with(@id, 'IdFirstName')]")))

    @allure.step("Initializing contact query")
    def get_passenger_suffixes(self):
        inputs = self.driver.find_elements(By.XPATH,"//input[starts-with(@id, 'IdFirstName')]")
        suffixes = [i.get_attribute("id").replace("IdFirstName", "") for i in inputs]
        return suffixes


    @allure.step("Select dropdown value: {field_type} = {value} for suffix {suffix}")
    def select_dropdown_value(self, suffix, field_type, value, birth_date=None, passenger_type=None):
        field_ids = {
            "day": "dateDayId_IdDateOfBirthHidden",
            "month": "dateMonthId_IdDateOfBirthHidden",
            "year": "dateYearId_IdDateOfBirthHidden"
        }

        if field_type not in field_ids:
            raise ValueError(f"Invalid field type: {field_type}. Must be 'day', 'month', or 'year'.")

        base_id = field_ids[field_type]
        dropdown = (By.ID, f"{base_id}_{suffix}_")
        if field_type == "month":
            visible_text = MONTH_NAMES.get(value)
            if not visible_text:
                raise ValueError(f"Invalid month number: {value}")
            option = (By.XPATH, f"//span[@class='ui-dropdown_item_option_name' and text()='{visible_text}']")
        elif field_type == "year":
            option = (By.XPATH, f"//span[@class='ui-dropdown_item_option_name' and text()='{value}']")
        else:
            option = (By.ID, f"{base_id}_{suffix}_-{value}")

        self.scroll_and_click(dropdown)
        try:
            self.wait.until(EC.presence_of_element_located(option))
        except TimeoutException:
            self.capture(f"{field_type.capitalize()} {value} not found for suffix {suffix}")
            raise Exception(f" {field_type.capitalize()} {value} not found in dropdown for suffix '{suffix}' (passenger type '{passenger_type}')")
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", self.driver.find_element(*option))
        except:
            self.capture(f"Failed to scroll to {field_type} value: {value}")
        self.scroll_and_click(option)
        self.capture(f"Select {field_type}: {value}")

        if birth_date and passenger_type:
            day, month, year = birth_date
            age = calculate_age(day, month, year)
            min_age, max_age = AGE_RANGES[passenger_type]
            if not (min_age <= age <= max_age):
                raise Exception(f"Invalid age for passenger type '{passenger_type}': {age} years")


    @allure.step("Enter passenger data {index}")
    def fill_passenger_info(self, index, suffix, first_name, last_name, gender, day, month, year, nationality_index, passenger_type):
        #  Usa el sufijo para construir los IDs dinámicos
        self.scroll_and_click((By.ID, f"IdPaxGender_{suffix}"))
        self.scroll_and_click((By.ID, f"IdPaxGender_{suffix}-{gender}" ))
        self.capture("Select gender")

        self.scroll_and_click((By.ID, f"IdFirstName{suffix}" ))
        self.send_keys((By.ID, f"IdFirstName{suffix}"), first_name)
        self.capture("Select name")

        self.scroll_and_click((By.ID, f"IdLastName{suffix}" ))
        self.send_keys((By.ID, f"IdLastName{suffix}"), last_name)
        self.capture("Select last name")

        birth_date = (day, month, year)
        self.select_dropdown_value(suffix, "day", day)
        self.select_dropdown_value(suffix, "month", month)
        self.select_dropdown_value(suffix, "year", year, birth_date=birth_date, passenger_type=passenger_type)

        self.scroll_and_click((By.ID, f"IdDocNationality_{suffix}"))
        self.scroll_and_click((By.ID, f"IdDocNationality_{suffix}-{nationality_index}"))
