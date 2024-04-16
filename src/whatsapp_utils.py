import time  # Provides various time-related functions.
import re  # Imports the regex module for regular expression operations.
import json  # Imports the JSON module to read/write JSON formatted data.
from selenium import webdriver  # Importing WebDriver for browser automation.
from selenium.webdriver.chrome.options import Options  # For setting options for the Chrome driver.
from selenium.webdriver.common.by import By  # For locating elements by their type.
from selenium.webdriver.common.keys import Keys  # For simulating keyboard keys.
from selenium.webdriver.support.ui import WebDriverWait  # For making Selenium wait for specific conditions.
from selenium.webdriver.support import expected_conditions as EC  # For specifying what to wait for in WebDriverWait.
from selenium.common.exceptions import ElementClickInterceptedException  # To catch exceptions for unclickable elements.


# Function to read configuration and get the chat name
def get_chat_name_from_config():
    try:
        with open('data/config.json', 'r') as json_file:
            config_data = json.load(json_file)
            return config_data['chat_name']
    except (FileNotFoundError, KeyError):
        print("Error reading chat name from config.json. Please ensure the 'chat_name' field exists.")
        raise
    
# Defines a function to open WhatsApp Web and login after scanning QR code.
def open_whatsapp_and_login():
    chrome_options = Options()  # Create an instance to set Chrome options.
    driver = webdriver.Chrome(options=chrome_options)  # Initialize the Chrome driver with the specified options.
    driver.get("https://web.whatsapp.com/")  # Directs the driver to open WhatsApp Web.
    print("Waiting for 15 seconds to let the QR code appear...")
    time.sleep(15)  # Wait for some time to let WhatsApp load and the QR code appear.
    wait_for_qr_code_scan(driver)  # Call function to wait until the QR code has been scanned.
    return driver  # Return the WebDriver instance for further interactions with WhatsApp Web.

# Defines a function that waits until the QR code has been scanned.
def wait_for_qr_code_scan(driver):
    qr_code_present = True  # Flag indicating whether the QR code is present.
    while qr_code_present:  # Loop as long as the QR code is present.
        try:
            # Look for the element that represents the QR code (canvas).
            driver.find_element(By.CSS_SELECTOR, 'canvas[aria-label="Scan me!"]')
            print("Waiting for QR code to be scanned...")
            time.sleep(5)  # Wait before trying again.
        except:
            qr_code_present = False  # If the element is not found, the QR code has been scanned.
    print("QR code has been scanned. Waiting for chats to sync...")  # Indicate that the QR code was successfully scanned.

# Defines a function to navigate to a chat given its name.
def navigate_to_chat(driver, chat_name):
    search_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]/p'))
    )  # Waits for the search box to be clickable.
    try:
        search_box.click()  # Attempt to click the search box.
    except ElementClickInterceptedException:
        # Use JavaScript click if regular click fails due to overlay issues.
        driver.execute_script("arguments[0].click();", search_box)
    search_box.clear()  # Clears the search box contents.
    search_box.send_keys(chat_name)  # Type the chat name into the search box.
    search_box.send_keys(Keys.ENTER)  # Simulate pressing Enter to confirm the chat search.
    time.sleep(4)  # Wait for chat messages to load.

# Defines a function to check the latest message in a chat for a Google Meet link.
def check_latest_message_for_meet_link(driver):
    messages = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]')
    if messages:
        latest_message = messages[-1].text  # Retrieves the last message's text.
        meet_code_pattern = r'(meet\.google\.com/[a-zA-Z0-9\-]+)'  # Regex pattern to find Google Meet links.
        found_links = re.findall(meet_code_pattern, latest_message)  # Finds all occurrences of the pattern.
        meet_links = ['https://' + link if not link.startswith('http') else link for link in found_links]
        # Prepends 'https://' to found codes if missing, otherwise leaves them unchanged.
        return meet_links  # Returns a list of properly formatted meet links.
    return []  # Returns an empty list if no messages were found.

# Defines a function to update the configuration file with the new Meet link.
def update_config_with_meet_link(meet_link):
    try:
        with open(r'data\config.json', 'r') as json_file:  # Attempts to open the config file in read mode.
            config_data = json.load(json_file)  # Loads the JSON data from the config file.
    except FileNotFoundError:
        config_data = {}  # If file not found, start with an empty config dictionary.
    config_data['meet_link'] = meet_link  # Updates/adds the Meet link to the config dictionary.
    with open(r'data\config.json', 'w') as json_file:  # Opens the config file in write mode.
        json.dump(config_data, json_file, indent=4)  # Writes the updated dictionary to the file.
    print("Meet link updated in config.json")  # Prints confirmation message.
