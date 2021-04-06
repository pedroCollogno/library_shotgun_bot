import os
import time

from dotenv import load_dotenv
from selenium import webdriver

load_dotenv()
SELENIUM_DRIVERS_PATH = os.environ.get("SELENIUM_DRIVERS_PATH")
CHROME_VERSION = os.environ.get("CHROME_VERSION")

driver = webdriver.Chrome(
    f"{SELENIUM_DRIVERS_PATH}/chrome_{CHROME_VERSION}_driver",)

LIBRARY_URL = "https://affluences.com/necker/reservation?type=1781"
driver.get(LIBRARY_URL)

driver.find_element_by_tag_name(
    "app-cookie-banner").find_element_by_tag_name("button").click()

resources = driver.find_elements_by_class_name("ressource")

for resource in resources:
    hour_grp = resource.find_element_by_class_name("hour-grp")
    available_slot = hour_grp.find_element_by_class_name("available")
    if available_slot:
        print(available_slot.text)
        available_slot.click()
        durations = resource.find_element_by_class_name("hour-group")
        biggest_duration = durations.find_element_by_class_name("last")
        print(biggest_duration.text)
        biggest_duration.click()
        book_button = resource.find_element_by_class_name("mat-button-wrapper")
        if book_button:
            book_button.click()
            time.sleep(10)
driver.close()
