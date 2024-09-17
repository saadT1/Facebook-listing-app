from selenium import webdriver
from pynput.keyboard import Key
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import json



# Load JSON data from file
with open('data.json') as f:
    data = json.load(f)

# Extract listings structure and general info
listings_structure = data['listings']


filename=data['filename']
print(filename)

with open('ids.json') as f:
    ids = json.load(f)


def load_state(user_id):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            state = json.load(file)
            return state.get(user_id, {'listed_items': {}})
    else:
        return {'listed_items': {}}

def save_state(user_id, state_data):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            state = json.load(file)
    else:
        state = {}

    state[user_id] = state_data

    with open(filename, 'w') as file:
        json.dump(state, file)

        
def wait_for_element_to_be_clickable(driver, locator, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
        element.click()
        print("Element clicked successfully!")
    except TimeoutException:
        print("Element was not clickable within the specified timeout.")

def limit(driver):
    time.sleep(2)
    try:
        driver.find_element(By.XPATH, "//span[text()='Limit reached']")
        print("Limit reached")
        return True
    except NoSuchElementException:
        return False
  
def next(driver):
    time.sleep(2)
    try:
        button=driver.find_element(By.XPATH, "//span[text()='Next']")
        button.click()
        
        print("Next button clicked successfully!")
    except NoSuchElementException:
        print("Next button was not found.")

        
def login(driver, user_id, password):
    driver.find_element(By.XPATH, "//div[@aria-label='Allow all cookies' and @tabindex='0']").click()
    driver.find_element(By.ID, "email").send_keys(user_id)
    driver.find_element(By.ID, "pass").send_keys(password)
    driver.find_element(By.ID, "loginbutton").click()


def setLoaction(driver,element_location,location):
   
    wait_for_element_to_be_clickable(driver, (By.XPATH, "//div[@id='seo_filters']"))
    time.sleep(3)
    button=driver.find_element(By.XPATH, "//input[@aria-label='Location']")
    button.click()
    time.sleep(2)
    button.send_keys(location)
    time.sleep(2)
    driver.find_element(By.XPATH,element_location).click()
    
  
def avalability(driver):
    try:
        availability=driver.find_element(By.XPATH, "//label[@aria-label='Availability']")
        time.sleep(1)
        availability.click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//div[@role='listbox']/div/div/div/div/div/div/div/following-sibling::div").click()
        time.sleep(2)
    except NoSuchElementException:
        print("Availability not found")
        


def add_listing(driver, image_path, title, price, category, description, location, element_location, category_id, category_id1, listing_name, item_number):
    
    image=driver.find_element(By.XPATH, "//input[@accept='image/*,image/heif,image/heic']")
    image.send_keys(image_path)
    time.sleep(3)
    driver.find_element(By.XPATH, "//label[@aria-label='Title']").send_keys(title)
    time.sleep(0.5)
    driver.find_element(By.XPATH, "//label[@aria-label='Price']").send_keys(price)
    time.sleep(0.5)
    driver.find_element(By.XPATH, "//label[@aria-label='Category']").send_keys(category)
    time.sleep(1)


    try:

       driver.find_element(By.XPATH, category_id).click()
    except NoSuchElementException:
         driver.find_element(By.XPATH, category_id1).click()

    time.sleep(0.5)
    driver.find_element(By.XPATH, "//label[@aria-label='Condition']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[@role='listbox']//span[text()='New']").click()
    time.sleep(0.5)
    desc=driver.find_element(By.XPATH, "//label[@aria-label='Description']")
    time.sleep(2)
    desc.send_keys(description)
    time.sleep(5)
    
    avalability(driver)
    time.sleep(1)

    button=driver.find_element(By.XPATH, "//input[@aria-label='Location']")
    button.click()
    time.sleep(2)
    button.send_keys(location)
    time.sleep(2)
    driver.find_element(By.XPATH,element_location).click()
    time.sleep(1)
    next(driver)
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[@aria-label='Publish']").click()
    time.sleep(5)
    print(f"Listing added successfully: {listing_name} - Item Number {item_number}")


def perform_listings_for_user(user_id, password, location):
    # Load user state
    user_state = load_state(user_id)
    listed_items = user_state.get('listed_items', {})

    # Check if all items are listed
    all_items_listed = True
    for category, items in data["listings"].items():
        if category not in listed_items:
            all_items_listed = False
            break
        for item_name, item_info in items.items():
            if item_name not in listed_items[category]:
                all_items_listed = False
                break
            item_numbers = item_info.get("no of listings", [])
            for item_number in item_numbers:
                if item_number not in listed_items[category][item_name]:
                    all_items_listed = False
                    break
            if not all_items_listed:
                break
        if not all_items_listed:
            break

    if all_items_listed:
        print(f"All items for user {user_id} are already listed. Skipping this user.")
        return

    # Proceed with the listing process
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://web.facebook.com/login")
    driver.maximize_window()
    login(driver, user_id, password)
    time.sleep(5)

    locationElement = f"//ul//span[text()='{location}']"
    driver.get("https://www.facebook.com/marketplace/?ref=bookmark")
    time.sleep(2)
    setLoaction(driver, locationElement, location)
    time.sleep(2)
    try:

        driver.find_element(By.XPATH, "//div[@aria-label='Apply']").click()

    except NoSuchElementException:

        print("Cookies not found")
        
    time.sleep(5)
    print(f"Location for user {user_id} set to {location}")

    for category, items in data["listings"].items():
        if category not in listed_items:
            listed_items[category] = {}

        for item_name, item_info in items.items():
            if item_name not in listed_items[category]:
                listed_items[category][item_name] = []

            item_numbers = item_info.get("no of listings", [])
            if not item_numbers:
                # Handle items without specific listing numbers
                item_numbers = [None]  # Use None to indicate no specific number

            for item_number in item_numbers:
                if item_number in listed_items[category][item_name]:
                    continue

                # Get the info for the item
                info = item_info.copy()  # make a copy to modify if needed
                if item_number is not None:
                    image_path = info["path"].format(item_number)
                else:
                    image_path = info["path"].replace("{}", "")
                info["location"] = location
                info["element_location"] = f"//ul//span[text()='{location}']"
                print(f"Listing: {category} - {item_name} - {item_number}")

                driver.get("https://www.facebook.com/marketplace/create/item/")
                time.sleep(5)

                if limit(driver):
                    break

                add_listing(
                    driver,
                    image_path,
                    info["title"],
                    info["price"],
                    info["category"],
                    info["description"],
                    info["location"],
                    info["element_location"],
                    info["id"],
                    info["id1"],
                    item_name,
                    item_number
                )
                time.sleep(10)
                listed_items[category][item_name].append(item_number)
                save_state(user_id, {'listed_items': listed_items})

            if limit(driver):
                break
        if limit(driver):
            break

    driver.quit()


def main():
    for user_id, user_info in ids.items():
        password = user_info['password']
        location = user_info['location']
        perform_listings_for_user(user_id, password, location)
        print(f"Completed listings for {user_id} in {location}")
        time.sleep(10) 


if __name__ == "__main__":
    main()