import json  # For parsing JSON files.
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

def activate_meet_window_by_click():
    """
    Attempts to bring the Google Meet window to the foreground by performing a click action with pyautogui.
    
    Searches through all open windows to find one associated with Google Meet and 'Google Chrome' in its title.
    If it finds one, it clicks on the window to activate it.

    :return: bool - True if the Meet window is successfully activated, False otherwise.
    """
    # Retrieve a list of all open windows that have "Meet" and "Google Chrome" in their title
    possible_meet_windows = [window for window in pyautogui.getAllWindows()
                             if "Meet" in window.title and "Google Chrome" in window.title]
    
    # Check if no Meet Chrome window was found
    if not possible_meet_windows:
        print("No Google Meet Chrome window found.")  # Inform the user that no window was detected
        return False  # Return False to indicate failure to find the Meet window
    
    # Activate the first Meet window found by moving the mouse over it and clicking
    meet_window = possible_meet_windows[0]  # Select the first window from the list of possible Meet windows
    win_center_x, win_center_y = meet_window.center  # Get the center X and Y coordinates of the window
    pyautogui.moveTo(win_center_x, win_center_y)  # Move the mouse pointer to the center of the window
    pyautogui.click()  # Perform a left mouse button click to activate the window
    print("Meet window activated by mouse click.")  # Inform the user that the window has been activated
    return True  # Return True to indicate success
