import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, 40)

    def capture(self, name):
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=AttachmentType.PNG
        )

    def wait_for_element(self, locator, label="wait element"):
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            self.capture(label)
        except Exception as e:
            self.capture(f"Error waiting {label}")
            raise e

    def scroll_and_click(self, locator, name="Scroll and click", timeout=50):
        try:
            local_wait = WebDriverWait(self.driver, timeout)
            local_wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script("""
                let container = document.querySelector('.services-wrapper') || document.querySelector('.modal-content');
                if (container) container.scrollTop = container.scrollHeight;
            """)
            elem = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
            time.sleep(1)
            if not elem.is_displayed():
                raise  Exception("Element is not displayed")
            if not elem.is_enabled():
                raise Exception("Element is not enabled")
            self.capture(name)
            local_wait.until(EC.element_to_be_clickable(locator))
            try:
                elem.click()
            except:
                ActionChains(self.driver).move_to_element(elem).click().perform()
            print(f"Scroll and click: {name}")
            return elem
        except Exception as e:
            self.capture(f"Error: {name}")
            print(f"Error: {e}")
            raise e

    def send_keys(self, locator, text):
        element = self.driver.find_element(*locator)
        element.clear()
        element.send_keys(text)

    def wait_for_loader(self, loader_class="page-loader"):
        self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, loader_class)))

