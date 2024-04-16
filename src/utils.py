import json# For parsing JSON files.
import time  
import pyautogui  # Import the pyautogui library for GUI automation tasks like mouse and keyboard control
from selenium.webdriver.support.ui import WebDriverWait  # Import WebDriverWait for waiting for elements to load
from selenium.webdriver.common.by import By  # Import By to specify how to locate elements in the page
from selenium.webdriver.support import expected_conditions as EC  # Import EC to define conditions for wait

# Define utility functions here

def load_config(filename):
    """Load configuration from a JSON file."""
    with open(filename, 'r') as file:  # Open the file in read mode.
        config = json.load(file)  # Load the contents of the file into a Python object.
    return config  # Return the read configuration.

def check_element_visibility(driver, xpath):
    """
    Checks if an element specified by its XPath is visible within the DOM of a page.

    :param driver: The Selenium WebDriver instance used to interact with the browser.
    :param xpath: The XPath string that identifies the element to check.
    :return: bool - True if the element is visible within the set timeout period, False otherwise.
    """
    try:
        # Wait up to 10 seconds for the element at the specified xpath to be visible on the page
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        return element.is_displayed()  # Return whether the element is displayed or not
    except:
        # In case of any exception (e.g., timeout or element not found), return False
        return False  # Return False if element is not found within the timeout period

def activate_meet_window_by_click(delay_seconds=1):
   time.sleep(delay_seconds)
   pyautogui.click(button='right')
