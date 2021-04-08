import json
import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


def parse_time(time_s):
    h, m = [int(s) for s in time_s.split(":")]
    return (h * 60) + m


load_dotenv()
SELENIUM_DRIVERS_PATH = os.environ.get("SELENIUM_DRIVERS_PATH")
CHROME_VERSION = os.environ.get("CHROME_VERSION")
PREFERENCES_FILE_PATH = "./preferences.json"

with open(PREFERENCES_FILE_PATH, "r") as f:
    preferences = json.load(f)
    preferences["min_hour"] = parse_time(preferences["min_hour"])
    preferences["max_hour"] = parse_time(preferences["max_hour"])

driver = webdriver.Chrome(
    f"{SELENIUM_DRIVERS_PATH}/chrome_{CHROME_VERSION}_driver",)
actions = ActionChains(driver)

LIBRARY_URL = "https://affluences.com/necker/reservation?type=1781"
driver.get(LIBRARY_URL)

input()

driver.find_element_by_tag_name(
    "app-cookie-banner").find_element_by_tag_name("button").click()

resources = driver.find_elements_by_class_name("ressource")

for resource in resources:
    hour_grp = resource.find_element_by_class_name("hour-grp")
    available_slots = hour_grp.find_elements_by_class_name("available")
    for slot in available_slots:
        try:
            hour = parse_time(slot.text)
            if hour >= preferences["min_hour"] and hour <= preferences["max_hour"]:
                available_slot = slot
                break
        except Exception as e:
            continue

    if available_slot:
        available_slot.click()
        durations = resource.find_element_by_class_name("hour-group")
        biggest_duration = durations.find_element_by_class_name("last")
        biggest_duration.click()
        book_button = resource.find_element_by_class_name("mat-button-wrapper")
        if book_button:
            book_button.click()

            email = driver.find_element_by_id("email")
            email.send_keys(preferences["email"])
            firstname = driver.find_element_by_id("firstname")
            firstname.send_keys(preferences["firstname"])
            lastname = driver.find_element_by_id("lastname")
            lastname.send_keys(preferences["lastname"])
            master = driver.find_element_by_id("note")
            master.send_keys(preferences["master"])
            checkbox = driver.find_element_by_id("agreementUser-input")
            actions.move_to_element(checkbox)
            actions.click(checkbox)
            actions.perform()

            submit = driver.find_element_by_class_name("btn-success")
            submit.click()
            break

input()
driver.close()
