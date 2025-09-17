from allure_commons.types import AttachmentType
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from selenium.webdriver.common.action_chains import ActionChains

class SelectFlightPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Select  flight {index}")
    def select_fare_by_index(self, index=1):
        try:
            self.wait_for_element((By.CLASS_NAME, "journey_price_button"))
            xpath = f"(//button[contains(@class, 'journey_price_button')])[{index}]"
            self.scroll_and_click((By.XPATH, xpath))
            self.capture("Select   flight {index}")
        except Exception as e:
            self.capture(f"Error select   flight {index}")
            raise e

    @allure.step("Select fare option at position {index}")
    def select_tariff_by_index (self, index=1):
        try:
            self.wait_for_element((By.CLASS_NAME, "fare_button"))
            xpath = f"(//button[contains(@class, 'fare_button')])[{index}]"
            self.scroll_and_click((By.XPATH, xpath))
            self.capture("Select tarif {index}")
        except Exception as e:
            self.capture(f"Error select tarif  {index}")
            raise e

    @allure.step("Click continue Button ")
    def click_continue_button(self, locator=(By.XPATH, "//*[@id='maincontent']/div/div[2]/div/div/button-container/div/div/button")):
        try:
            self.wait_for_loader()
            self.wait.until(EC.presence_of_element_located(locator))
            self.wait.until(EC.visibility_of_element_located(locator))
            try:
                self.scroll_and_click(locator)
            except:
                elem = self.driver.find_element(*locator)
                ActionChains(self.driver).move_to_element(elem).click().perform()
            #self.capture("Click continue Button ")
            print("Search button is clicked successfully")
        except Exception as e:
            self.capture(f"Error click continue button {locator}")
            print(f"Error clicking search button: {e}")
            raise e





