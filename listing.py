from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import streamlit as st
import os
import random
import json

USER_DATA_FILE_PATH = "ids.json"
LISTINGS_DATA_FILE_PATH = "data.json"


# Load JSON data from file
def load_user_data():
    if not os.path.exists(LISTINGS_DATA_FILE_PATH):
        with open(LISTINGS_DATA_FILE_PATH, "w") as file:
            json.dump({}, file)  # Create an empty JSON file

    with open(LISTINGS_DATA_FILE_PATH, "r") as file:
        return json.load(file)


data = load_user_data()
listings_structure = data["listings"]

filename = "round1.json"


with open("ids.json") as f:
    ids = json.load(f)


def load_state(user_id):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            state = json.load(file)
            return state.get(user_id, {"listed_items": {}})
    else:
        return {"listed_items": {}}


def save_state(user_id, state_data):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            state = json.load(file)
    else:
        state = {}

    state[user_id] = state_data

    with open(filename, "w") as file:
        json.dump(state, file)


def load_state(user_id):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            state = json.load(file)
            return state.get(user_id, {"listed_items": {}})
    else:
        return {"listed_items": {}}


def save_state(user_id, state_data):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            state = json.load(file)
    else:
        state = {}

    state[user_id] = state_data

    with open(filename, "w") as file:
        json.dump(state, file)


def wait_for_element_to_be_clickable(driver, locator, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        print("Element clicked successfully!")
    except TimeoutException:
        print("Element was not clickable within the specified timeout.")


def limit(driver):
    try:
        driver.find_element(By.XPATH, "//span[text()='Limit reached']")
        print("Limit reached")
        return True
    except NoSuchElementException:
        return False


def next(driver):
    try:
        driver.click_if_visible(By.XPATH, "//span[text()='Next']", timeout=2)

        print("Next button clicked successfully!")
    except NoSuchElementException:
        print("Next button was not found.")


def login(driver, user_id, password):
    driver.find_element(
        By.XPATH, "//div[@aria-label='Allow all cookies' and @tabindex='0']"
    ).click()
    username = driver.find_element(By.XPATH, "//input[@name='email']")
    passw = driver.find_element(By.XPATH, "//input[@name='pass']")
    for char in user_id:
        username.send_keys(char)
        time.sleep(random.uniform(0.1, 0.5))
    for char in password:
        passw.send_keys(char)
        time.sleep(random.uniform(0.1, 0.5))

    driver.click_if_visible(
        "//button[@id='loginbutton']", timeout=time.sleep(random.uniform(0.5, 2))
    )


def setLoaction(driver, element_location, location):
    driver.click_if_visible(By.XPATH, "//div[@id='seo_filters']", timeout=10)
    time.sleep(3)
    button = driver.find_element(By.XPATH, "//input[@aria-label='Location']")
    button.click()
    time.sleep(2)
    button.send_keys(location)
    time.sleep(2)
    driver.find_element(By.XPATH, element_location).click()


def avalability(driver):
    try:
        availability = driver.find_element(
            By.XPATH, "//label[@aria-label='Availability']"
        )
        time.sleep(1)
        availability.click()
        time.sleep(3)
        driver.find_element(
            By.XPATH,
            "//div[@role='listbox']/div/div/div/div/div/div/div/following-sibling::div",
        ).click()
        time.sleep(2)
    except NoSuchElementException:
        print("Availability not found")


def add_listing(
    driver,
    image_path,
    title,
    price,
    category,
    description,
    location,
    element_location,
    category_id,
    category_id1,
    listing_name,
    item_number,
):

    image = os.path.abspath(image_path)
    driver.send_keys(
        "//input[@accept='image/*,image/heif,image/heic']", image, timeout=5
    )
    time.sleep(2)
    driver.send_keys(
        "//span[text()='Title']/following-sibling::input", title, timeout=5
    )
    time.sleep(2)
    driver.send_keys(
        "//span[text()='Price']/following-sibling::input", price, timeout=5
    )
    time.sleep(2)
    driver.send_keys(
        "//span[text()='Category']/following-sibling::input", category, timeout=5
    )
    time.sleep(2)
    try:
        driver.click_if_visible(f"//li[@id='{category_id}']", timeout=2)
    except NoSuchElementException:
        driver.click_if_visible(f"//li[@id='{category_id}']", timeout=2)
    driver.click_if_visible(
        "//span[text()='Condition']/following-sibling::div", timeout=5
    )
    time.sleep(1)
    driver.click_if_visible("//div[@role='listbox']//span[text()='New']", timeout=5)
    time.sleep(2)
    driver.type(
        "//span[text()='Description']/following-sibling::div/textarea",
        description,
        timeout=5,
    )

    avalability(driver)
    time.sleep(1)

    driver.type("//input[@aria-label='Location']", location, timeout=5)
    time.sleep(2)
    driver.click_if_visible(element_location, timeout=5)
    next(driver)
    driver.click_if_visible(By.XPATH, "//span[text()='Publish']", timeout=5)
    time.sleep(2)


def perform_listings_for_user(user_id, password, location):
    # Load user state
    user_state = load_state(user_id)
    listed_items = user_state.get("listed_items", {})

    # Check if all items are listed
    all_items_listed = True
    for category, subcategories in listings_structure.items():
        if category not in listed_items:
            all_items_listed = False
            break
        for subcategory, item_info in subcategories.items():
            if subcategory not in listed_items[category]:
                all_items_listed = False
                break
            listed_numbers = listed_items[category][subcategory]
            item_numbers = item_info.get("no of listings", [])
            if not item_numbers:
                if None not in listed_numbers:
                    all_items_listed = False
                    break
            else:
                for item_number in item_numbers:
                    if item_number not in listed_numbers:
                        all_items_listed = False
                        break
                else:
                    continue
                break
        else:
            continue
        break

    if all_items_listed:
        print(f"All items for user {user_id} are already listed. Skipping this user.")
        return

    # Proceed with the listing process
    chrome_options = ["--disable-notifications"]
    driver = Driver(browser="chrome", chromium_arg=["--disable-notifications"], uc=True)
    driver.maximize_window()
    driver.open("https://web.facebook.com/login")

    login(driver, user_id, password)
    driver.wait_for_element_visible("//a[@aria-label='Home']", timeout=20)

    driver.open("https://www.facebook.com/marketplace/?ref=bookmark")
    locationElement = f"//ul//span[text()='{location}']"
    setLoaction(
        driver, locationElement, location
    )  # Fixed typo: setLoaction -> setLocation
    driver.find_element(By.XPATH, "//div[@aria-label='Apply']").click()
    driver.click_if_visible("//div[@aria-label='Apply']", timeout=10)
    st.write(f"Location for user {user_id} set to {location}")
    title_counter = 0

    for category, subcategories in listings_structure.items():
        if category not in listed_items:
            listed_items[category] = {}
        for subcategory, item_info in subcategories.items():
            if subcategory not in listed_items[category]:
                listed_items[category][subcategory] = []
            item_numbers = item_info.get("no of listings", [])
            if not item_numbers:
                item_numbers = [None]
            for item_number in item_numbers:
                if item_number in listed_items[category][subcategory]:
                    continue

                info = item_info.copy()
                # Handle image_path when item_number is None
                image_path = (
                    info["path"].format(item_number)
                    if item_number is not None
                    else info["path"].replace(" {}", "")
                )
                info["location"] = location
                info["element_location"] = f"//ul//span[text()='{location}']"
                st.write(f"Listing: {category} - {subcategory} - {item_number}")
                driver.open("https://www.facebook.com/marketplace/create/item/")
                if limit(driver):
                    break
                current_title = info["title"][title_counter % len(info["title"])]
                title_counter += 1

                def filter_non_bmp(text):
                    return "".join(c for c in text if ord(c) <= 0xFFFF)

                filtered_title = filter_non_bmp(current_title)
                st.write(f"Image path: {image_path}")
                add_listing(
                    driver,
                    image_path,
                    filtered_title,
                    info["price"],
                    info["category"],
                    info["description"],
                    info["location"],
                    info["element_location"],
                    info["id"],
                    info["id1"],
                    subcategory,
                    item_number,
                )
                time.sleep(5)
                driver.click_if_visible('//div[@aria-label="Publish"]', timeout=10)
                time.sleep(10)
                listed_items[category][subcategory].append(item_number)
                save_state(user_id, {"listed_items": listed_items})
            if limit(driver):
                break
        if limit(driver):
            break

    driver.quit()


def listing():
    for user_id, user_info in ids.items():
        password = user_info["password"]
        location = user_info["location"]
        perform_listings_for_user(user_id, password, location)
        st.success(f"Completed listings for {user_id} in {location}")
        time.sleep(10)


if __name__ == "__main__":
    listing()
