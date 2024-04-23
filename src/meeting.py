# Import necessary modules for the script's functionality
from selenium import webdriver  # Provides WebDriver base class needed to instantiate a new browser.
from selenium.common.exceptions import TimeoutException, NoSuchWindowException  # To catch timeouts during wait periods.
from selenium.webdriver.support.ui import WebDriverWait  # Enables use of WebDriverWait.
from selenium.webdriver.common.by import By  # For locating elements by their HTML attributes.
from selenium.webdriver.support import expected_conditions as EC  # Allows waiting for certain conditions.
import time

def setup_driver(config):
    """Setup Chrome WebDriver with hardcoded options."""
    
    chrome_options = webdriver.ChromeOptions()  # Instantiate an Options object for ChromeDriver.

    # Set user-defined preferences such as disabling notifications and location requests.
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.geolocation": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)  # Add prefs to ChromeOptions.

    # Add command-line arguments to ChromeOptions for additional configurations.
    args = [
        "--no-first-run",
        "--no-service-autorun",
        "--start-maximized",
        "--password-store=basic"
    ]
    for arg in args:
        chrome_options.add_argument(arg)  # Add each argument from the list.

    # Disable logging.
    exclude_switches = ["enable-logging"]
    chrome_options.add_experimental_option('excludeSwitches', exclude_switches)

    # Disable the automation extension (e.g., for bot detection mitigation).
    use_automation_extension = False
    chrome_options.add_experimental_option('useAutomationExtension', use_automation_extension)
    
    # Create a new instance of Chrome using the configured options.
    return webdriver.Chrome(options=chrome_options)

def login_to_google_meet(driver, config):
    """Perform login and join the meeting."""
    driver.get("https://meet.google.com/")  # Navigate to Google Meet homepage.

    try:
        wait = WebDriverWait(driver, 10)  # Set up WebDriverWait with a timeout of 10 seconds.

        # Execute actions to perform login sequence according to provided locators in the configuration.
        wait.until(EC.element_to_be_clickable((By.XPATH, config['sign_in_button_locator']))).click()
        email_input = wait.until(EC.presence_of_element_located((By.NAME, config['email_input_locator'])))
        email_input.send_keys(config['gmail_id'])
        wait.until(EC.element_to_be_clickable((By.XPATH, config['next_button_identifier_locator']))).click()
        password_input = wait.until(EC.presence_of_element_located((By.NAME, config['password_input_locator'])))
        password_input.send_keys(config['password'])
        wait.until(EC.element_to_be_clickable((By.XPATH, config['next_button_password_locator']))).click()

        # Enter the meeting by filling in the meet link and clicking the join buttons while muting audio/video.
        wait.until(EC.presence_of_element_located((By.XPATH, config['link_input_locator']))).send_keys(config['meet_link'])
        wait.until(EC.element_to_be_clickable((By.XPATH, config['join_button_locator']))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, config['mute_button_locator']))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, config['join_now_button_locator']))).click()

        # Loop to check for admission into the meeting every 10 seconds
        admitted = False
        start_time = time.time()
        max_wait_time = 300  # Maximum wait time (in seconds) for being admitted to the meeting
        wait_interval = 10   # Time interval between checks

        # Initialize WebDriverWait with a specified interval
        wait = WebDriverWait(driver, wait_interval)

        while not admitted and (time.time() - start_time) < max_wait_time:
            try:
                print("Checking if admitted to the meeting...")
                # Adjust the waiting time if necessary depending on the responsiveness of the page
                wait.until(EC.visibility_of_element_located((By.XPATH, config['meeting_ui_element_locator'])))
                print("Element found: admitted to the meeting!")
                admitted = True
            except TimeoutException:
                # Print the attempt and wait for 10 seconds before checking again
                print(f"Attempt unsuccessful. Trying again in {wait_interval} seconds...")
                time.sleep(wait_interval)

        if not admitted:
            raise TimeoutException("Timed out waiting for admission into the meeting.")
        
        print("Joined the meeting successfully.")

    except TimeoutException:
        print("Timed out waiting for a UI element.")
        driver.quit()  # Close the browser and end session upon encountering a timeout.

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        driver.quit()  # Close the browser upon any other exception.

def get_num_participants(driver):
    try:
        wait = WebDriverWait(driver, 10)  # Set up WebDriverWait with a timeout of 10 seconds.
        participant_count_locator = (By.XPATH, '//*[@id="yDmH0d"]//div[@class="uGOf1d"]')  # XPath locator for participant count.
        
        # Ensure the driver has not lost the window it interacts with
        print(f"Current window handle: {driver.current_window_handle}")  # This line prints the current window handle.

        participant_count_element = wait.until(EC.visibility_of_element_located(participant_count_locator))  # Wait for the participant count element to become visible.
        num_participants = int(participant_count_element.text)  # Parse the text as an integer.
        print(f"Number of participants: {num_participants}")
        return num_participants  # Return the number of participants.

    except NoSuchWindowException:
        print("The window was closed manually or has otherwise become unavailable.")
        return 0  # Return 0 if the window is not available.

    except TimeoutException:
        print("Timed out waiting for the participants count to appear.")  # Print message on timeout.

    except Exception as e:
        print(f"An error occurred: {e}")  # Catch-all for any other exceptions that may occur.
    
    return 0  # Return 0 by default if there was an issue fetching the participant count.

def leave_meeting(driver):
    try:
        wait = WebDriverWait(driver, 10)  # Set up WebDriverWait with a timeout of 10 seconds.
        hangup_button_locator = (By.XPATH, '//*[@id="yDmH0d"]//button[contains(@aria-label,"Leave call")]')  # Locator for the leave call button.
        hangup_button = wait.until(EC.element_to_be_clickable(hangup_button_locator))  # Wait for the button to be clickable.
        hangup_button.click()  # Click the button to leave the meeting.
        print("Left the meeting successfully.")

    except TimeoutException:
        print("Timed out waiting for the leave call button to appear")  # Message on button appearance timeout.

    except Exception as e:
        print(f"An error occurred while trying to leave the meeting: {e}")  # Catch-all for other exceptions leaving the meeting.
