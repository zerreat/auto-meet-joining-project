import subprocess  # To spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
import time  # Provides various time-related functions.
from whatsapp_utils import *  # Imports all functions from the module 'whatsapp_utils'.
from selenium.common.exceptions import TimeoutException  # To catch timeouts during wait periods in Selenium.

# Defines a function to fetch a Google Meet link from a specified WhatsApp chat.
def fetch_meet_link_from_whatsapp(chat_name):
    driver = open_whatsapp_and_login()  # Use utility function to open WhatsApp Web and login.
    navigate_to_chat(driver, chat_name)  # Navigate to the specified chat by name.
    meet_code_found = False  # Initialize a flag to check if the meet code has been found.

    while not meet_code_found:  # Repeat until a Meet code is found.
        meet_codes = check_latest_message_for_meet_link(driver)  # Check the latest messages for meeting codes.
        if meet_codes:  # If any meet codes are found.
            meet_code = meet_codes[0]  # Take the first meet code.
            print("Google Meet code found:", meet_code)  # Print confirmation that the code was found.
            update_config_with_meet_link(meet_code)  # Update the configuration with the new meet link.
            meet_code_found = True  # Set the flag to true since the meet code was found.
            driver.quit()  # Close the WebDriver.
            subprocess.run(["python", "src\meet_automation.py"])  # Run another Python script to automate the Google Meet process.
        else:
            # If no codes were found or there are no new messages, print status and wait before checking again.
            print("No Google Meet code found or no new messages. Checking again...")
            time.sleep(5)  # Wait for 5 seconds before trying again.

# This conditional ensures that the following code only runs when the script is executed directly, not when imported.
if __name__ == "__main__":
    try:
        chat_name = get_chat_name_from_config()  # Fetch the chat name from the config file.
        fetch_meet_link_from_whatsapp(chat_name)  # Use the fetched chat name here.
    except TimeoutException as e:
        # Catch timeout exceptions and print an informative message.
        print("An element could not be located within the specified time:")
        print(e.msg)
    except Exception as e:
        # Catch all other exceptions, print an informative message, and the exception itself.
        print("An error occurred:")
        print(str(e))
