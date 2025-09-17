import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.Contact_Page import ContactPage
from pages.search_page import SearchPage
from pages.select_flight_page import SelectFlightPage
from datetime import datetime
from random import randint
from utils.passenger_utils import (
        generate_date_of_birth,
        validate_age_by_type,
        map_types_by_code
)
import allure

def test_search_flow(driver):
    driver.get("https://av-booking-dev.newshore.es/es/")
    search = SearchPage(driver)
    search.accept_cookies((By.ID,"onetrust-accept-btn-handler"))
    search.capture("Accept Cookies")
    search.select_origin("Medellin", "MDE")
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "arrivalStationInputId")))
    search.select_destination("Bogota", "BOG")
    search.select_date_origin("22-10-2025")
    search.select_date_destination("26-10-2025")
    #search.select_passengers_by_type(passenger_type=1) #passengers by type
    search.select_passengers_dynamic([1,1,2,3])
    code_passengers = [1,2,1,3]
    type_for_passengers = map_types_by_code(code_passengers)
    search.validate_total_passengers(5)
    search.click_search_button()

    # select fligth
    select = SelectFlightPage(driver)
    select.select_fare_by_index(index=1)
    select.select_tariff_by_index(index=2)
    select.select_fare_by_index(index=29)
    select.select_tariff_by_index(index=2)
    select.click_continue_button()

    # Contacts
    contact = ContactPage(driver)
    contact.wait_for_contact_page()
    suffixes = contact.get_passenger_suffixes()

    first_names = ["Santiago", "Emilio", "Caro", "Alejo"]
    last_names = ["Gomez", "Lopez", "Torres", "Ramirez"]

    for i, suffix in enumerate(suffixes):
        passenger_type = type_for_passengers[i]
        day, month, year = generate_date_of_birth(passenger_type)

        contact.fill_passenger_info(
            index=i,
            suffix=suffix,
            first_name=first_names[i],
            last_name=last_names[i],
            gender=0,
            day=day,
            month=month,
            year=year,
            nationality_index=0,
            passenger_type=passenger_type
        )


