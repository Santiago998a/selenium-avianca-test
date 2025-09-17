from allure_commons.types import AttachmentType
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class SearchPage(BasePage):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        super().__init__(driver)

    #def capture(self, name):
     #   allure.attach(
      #      self.driver.get_screenshot_as_png(),
       #     name=name,
        #    attachment_type=AttachmentType.PNG,
        #)

    @allure.step("Accept Cookies")
    def accept_cookies(self, locator=(By.ID, "onetrust-accept-btn-handler")):
        try:
            elements = self.driver.find_elements(*locator)
            if elements:
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator)).click()
                self.capture("Accept Cookies")
        except Exception as e:
           if hasattr(self, "capture"):
            self.capture("Error accepting cookies")
            print(f"Error accepting cookies: {e}")
            raise e

    @allure.step("Select origen: {city} ({code})")
    def select_origin(self, city, code):
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, "originBtn")))
            self.wait.until(EC.element_to_be_clickable((By.ID, "originBtn"))).click()
            origin_input = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "departureStationInputId")))
            origin_input.click()
            origin_input.send_keys(city)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, code))).click()
            self.capture(f"Select origen ({city}, {code})")
        except Exception as e:
            if hasattr(self, "capture"):
                self.capture("Error selecting origin")
            print(f"Error selecting origin: {e}")
            raise e

    @allure.step("Select destination: {city} ({code})")
    def select_destination(self, city, code):
        try:
            destination_input = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "arrivalStationInputId")))
            destination_input.click()
            destination_input.send_keys(city)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, code))).click()
            self.capture("Select destination ({city}, {code})")
        except Exception as e:
            if hasattr(self, "capture"):
                self.capture("Error selecting destination")
            print(f"Error selecting destination: {e}")
            raise e

    @allure.step("Select date origen: {departure_data_str} ")
    def select_date_origin(self, departure_data_str):
        try:
            departure_date = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "departureDateButtonId")))
            departure_date.click()
            date_field =  WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[@aria-label='{departure_data_str}']")))
            date_field.click()
            self.capture(f"Select date origen ({departure_data_str})")
        except Exception as e:
            if hasattr(self, "capture"):
                self.capture("Error selecting date origin")
            print(f"Error selecting departure date: {e}")
            raise e

    @allure.step("Select date destination: {arrival_data_str} ")
    def select_date_destination(self, arrival_data_str):
        try:
            #arrival_date = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "arrivalStationInputId")))
            #arrival_date.click()
            date_field1 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[@aria-label='{arrival_data_str}']")))
            date_field1.click()
            self.capture(f"Select date destination ({arrival_data_str})")
        except Exception as e:
            if hasattr(self, "capture"):
                self.capture("Error selecting date destination")
            print(f"Error selecting return date: {e}")
            raise e

    @allure.step("Open selector of passengers ")
    def open_selector_passengers(self):
        try:
            self.driver.find_element(By.XPATH, "//button[contains(@class, 'control_field_button') and contains(@aria-label, 'Pasajeros :1')]").click()
            self.capture(f"Open selector of passengers")
        except Exception as e:
            print(f"Error opening passenger selector: {e}")

    @allure.step("select passenger {passenger_type}")
    def select_passengers_by_type(self, passenger_type):
        try:
            self.driver.find_element(By.XPATH, f"(//ibe-minus-plus//button[contains(@class, 'plus')])[{passenger_type}]").click()
            self.capture(f"Select passenger {passenger_type}")
        except Exception as e:
            print(f" Error selecting passenger type {passenger_type}: {e}")

    @allure.step(f"Select passenger dynamic")  #Esta funcion me sirve para probar multiples pasajeros
    def  select_passengers_dynamic(self, types):
        try:
            #self.open_selector_passengers()
            for passenger_type in types:
                self.select_passengers_by_type(passenger_type)
            expected_count  = len(types)
            self.validate_total_passengers(expected_count)
            self.capture("Select passenger dynamic")
        except Exception as e:
            print(f"  Error during dynamic passenger selection: {e}")

    @allure.step("validation of passengers {expected_count}")
    def validate_total_passengers(self, expected_count):
        try:
            passenger_button = self.driver.find_element(By.XPATH,"//button[contains(@class, 'control_field_button') and contains(@aria-label, 'Pasajeros :1')]")
            text = passenger_button.text.strip()
            assert f"{expected_count} passengers" in text, f" Expected  '{expected_count} passengers',  but found: '{text}'"
            print(f" Passenger count validated: {text}")
            self.capture("Passenger count validated")
        except Exception as e:
            print(f"Error validating passenger count: {e}")

    @allure.step("Click search button {locator}")
    def click_search_button(self, locator=(By.ID,"searchButton")):
        try:
            self.driver.find_element(*locator).click()
            self.capture(f"Click search button {locator}")
            print("Search button is clicked successfully")
        except Exception as e:
            print(f"Error clicking search button: {e}")








