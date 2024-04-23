import time
from utils import *  # Import all utility functions
from recording import *  # Import all recording-related functions
from meeting import *  # Import all meeting-related functions
from selenium.common.exceptions import WebDriverException, NoSuchWindowException

def main():
    try:
        config = load_config(r'data\config.json')  # Load configuration from JSON file
        driver = setup_driver(config)  # Set up the Selenium WebDriver with the imported configuration
        
        try:
            login_to_google_meet(driver, config)  # Function to log into Google Meet
            
            # Initialize recording control variable and XPath variables from configuration
            should_record = False
            xpath_1 = config['xpath_1']
            xpath_2 = config['xpath_2']

            while True:  # Loop indefinitely until exit conditions are met
                try:
                    num_participants = get_num_participants(driver)  # Fetch current number of participants
                except Exception as e:
                    print(f"An error occurred while getting the number of participants: {e}")
                    continue

                # Check if recording should start based on participant count
                if not should_record and num_participants >= 2:
                    start_recording()  # Start recording function
                    should_record = True  # Set flag indicating recording is underway
                    print("Recording has started")  # Print statement when recording starts

                # Execute if currently recording
                if should_record:
                    # If participants fall to one or none, stop recording and leave the meeting
                    if num_participants <= 1:
                        stop_recording()  # Stop the ongoing recording
                        print("Recording has stopped as there is only one participant.")  # Print statement when recording stops
                        leave_meeting(driver)  # Exit the meeting
                        break  # Break out of the loop to end execution
                    # If certain webpage elements become visible, also stop recording
                    elif check_element_visibility(driver, xpath_1) or check_element_visibility(driver, xpath_2):
                        stop_recording()  # Stop recording based on configured XPath visibility
                        print("Recording has stopped due to visibility conditions.")  # Print when recording stops based on visibility
                        
                time.sleep(5)  # Wait for a short period before repeating the actions in the loop

        except NoSuchWindowException:
            # Handle scenario where the browser window is closed unexpectedly or manually
            print("The window was closed manually or has otherwise become unavailable.")
        except WebDriverException as e:
            # Handle generic WebDriver exception and display the error message
            print(f"A WebDriver error occurred: {e}")
        finally:
            # Attempt to close the WebDriver session gracefully
            if driver:
                driver.quit()
            print("WebDriver session has been terminated.")

    except Exception as e:
        # Handle other exceptions that might occur outside the WebDriver interactions
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()  # Only run the main function when this script is executed directly
