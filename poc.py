import json
import os
import time

from dotenv import load_dotenv
import schedule
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from utils import parse_time

load_dotenv()
SELENIUM_DRIVERS_PATH = os.environ.get("SELENIUM_DRIVERS_PATH")
CHROME_VERSION = os.environ.get("CHROME_VERSION")
PREFERENCES_FILE_PATH = "./preferences.json"

with open(PREFERENCES_FILE_PATH, "r") as f:
    preferences = json.load(f)
    preferences["min_hour"] = parse_time(preferences["min_hour"])
    preferences["max_hour"] = parse_time(preferences["max_hour"])

driver = webdriver.Chrome(
    f"{SELENIUM_DRIVERS_PATH}/chrome_{CHROME_VERSION}_driver",
)
actions = ActionChains(driver)
LIBRARY_URL = "https://affluences.com/necker/reservation?type=1781"
TODAY = time.strftime("%d/%m/%Y", time.localtime(time.time()))
START_AT = time.strptime(
    f"{TODAY} {preferences['start_trying_at']}", "%d/%m/%Y %H:%M:%S")
MAX_JOB_TRIES = 3


def load_page():
    """
    Load the library's home page, close the cookies banner.
    """
    driver.get(LIBRARY_URL)
    try:
        banner = driver.find_element_by_tag_name("app-cookie-banner")
        banner.find_element_by_tag_name("button").click()
    except NoSuchElementException:
        pass


def get_resources():
    """
    Fetch the "ressource" elements (aka the different locations in the library).
    """
    max_retries = 10
    time_to_wait_between_tries = 1
    for _ in range(max_retries):
        try:
            resources = driver.find_elements_by_class_name("ressource")
            return resources
        except NoSuchElementException:
            time.sleep(time_to_wait_between_tries)
    raise NoSuchElementException


def find_available_slot_in_resource(resource):
    """
    Find available slot in given resource Element.
    Ensure that the user preferences are respected (not too early, not too late).
    If no spot is found, return False.
    Input:
        resource (selenium.webdriver.remote.webelement.WebElement): The DOM Node to explore.
    """
    available_slot = False
    hour_grp = resource.find_element_by_class_name("hour-grp")
    available_slots = hour_grp.find_elements_by_class_name("available")
    for slot in available_slots:
        try:
            hour = parse_time(slot.text)
            if hour >= preferences["min_hour"] and hour <= preferences["max_hour"]:
                available_slot = slot
                break
        except Exception:
            print(f"Error while parsing time string {slot.text}")
            continue

    return available_slot


def select_duration_for_slot(available_slot, resource):
    """
    Pick and click on the slot and the maximum duration for this slot.
    Input:
        - available_slot (selenium.webdriver.remote.webelement.WebElement): the DOM Node in which the buttons are.
        - resource (selenium.webdriver.remote.webelement.WebElement): The parent "ressource" DOM Node.
    """
    available_slot.click()
    durations = resource.find_element_by_class_name("hour-group")
    biggest_duration = durations.find_element_by_class_name("last")
    biggest_duration.click()


def fill_form_with_preferred_info():
    """
    Fill info form with info given in the "preferences.json" file, then submit the form.
    """
    email = driver.find_element_by_id("email")
    email.send_keys(preferences["email"])
    firstname = driver.find_element_by_id("firstname")
    firstname.send_keys(preferences["firstname"])
    lastname = driver.find_element_by_id("lastname")
    lastname.send_keys(preferences["lastname"])
    master = driver.find_element_by_id("note")
    master.send_keys(preferences["master"])
    for _ in range(10):
        try:
            checkbox = driver.find_element_by_id("agreementUser-input")
            actions.move_to_element(checkbox)
            actions.click(checkbox)
            actions.perform()

            submit = driver.find_element_by_class_name("btn-success")
            submit.click()
            break
        except Exception as e:
            print("Going too fast...")
            time.sleep(1)


def confirm_success():
    return True


def find_and_book_available_slot():
    success = False
    try:
        resources = get_resources()
    except NoSuchElementException:
        print("No resource found. Aborting.")
        raise RuntimeError("No resource found.")

    for resource in resources:
        try:
            available_slot = find_available_slot_in_resource(resource)

            if available_slot:
                select_duration_for_slot(available_slot, resource)
                book_button = resource.find_element_by_class_name(
                    "mat-button-wrapper")
                if book_button:
                    book_button.click()

                    fill_form_with_preferred_info()
                    success = confirm_success()
                    raise RuntimeError("oijzefoij")
                    break
        except NoSuchElementException:
            print("No available slot")
            continue

    return success


done = False
job_tries = 0

start = time.time()


def recurring_job():
    global done, job_tries
    load_page()
    done = find_and_book_available_slot()
    job_tries += 1


schedule.every(30).seconds.do(recurring_job)
while not done and job_tries < MAX_JOB_TRIES:
    if time.localtime() > START_AT:
        schedule.run_pending()
        time.sleep(5)

driver.close()
