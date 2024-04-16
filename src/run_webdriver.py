# The selenium.webdriver module provides the WebDriver implementations. Here, Chrome is used.
from selenium import webdriver
# Options class from selenium.webdriver.chrome.options helps to set various configurations for ChromeDriver.
from selenium.webdriver.chrome.options import Options

def main():
    # Create an instance of Options.
    chrome_options = Options()
    # Initialize the Chrome WebDriver with the optional settings (if any).
    driver = webdriver.Chrome(options=chrome_options)
    # Direct the WebDriver to navigate to the specified URL (Google Meet homepage in this case).
    driver.get("https://meet.google.com/")
    
    # This input function serves as a way for the user to signal when to end the WebDriver session.
    # The program will wait until the user presses Enter before proceeding.
    input("Press Enter to quit the WebDriver session...")

    # Once Enter is pressed, the WebDriver will close the Chrome window and end its session, releasing the resources it used.
    driver.quit()

# The following conditional checks if this script is being run directly, 
# meaning it's not being imported as a module into another Python script.
# __name__ is a special Python variable that equals '__main__' when the script is run directly.
if __name__ == '__main__':
    # If the script is run directly, the main function is called.
    main()
