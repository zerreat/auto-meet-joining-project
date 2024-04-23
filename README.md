# Auto Meet Joining Project

## Description

The Auto Meet Joining Project is a Python-based automation tool designed to fetch Google Meet links from specified WhatsApp chats, log into the meetings, and record them. This script utilizes Selenium WebDriver for browser automation to interact with WhatsApp Web, locate conversations, extract meet links, and initiate a separate script for meeting automation.

## Key Features

- Automatically fetches Google Meet links from WhatsApp messages.
- Records Google Meet sessions with minimal manual intervention.
- Logs into meetings seamlessly.
- Utilizes headless browser automation for unobtrusive operation.

## Prerequisites

Ensure the following are installed to run this script:
  
- Python 3.x
- Google Chrome Browser
- ChromeDriver (compatible with your Chrome version)

Install the required Python packages by running:

```bash
pip install -r requirements.txt
```

## Installation

Clone the repository to your local machine using:

```bash
git clone https://github.com/zerreat/auto-meet-joining-project.git
```

Navigate to the project directory:
```bash
cd auto-meet-joining-project
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Update Notice

We are currently working on a new feature that will allow users to directly log in using Google OAuth 2.0 `credentials.json`. This upcoming update will facilitate the process of obtaining a token and subsequently using it to interact with Google Meet. Please note that this feature is a work in progress, and it might take some time before it becomes available. We appreciate your patience and look forward to bringing you this enhancement.

## Configuration

Before running the script, there are a few preparatory steps necessary to ensure the software functions properly:

1. ###**Chrome WebDriver:**
   - Download the appropriate version of Chrome WebDriver based on the version of Google Chrome installed on your computer. To find your Chrome version, go to `chrome://settings/help` in your browser.
   - Visit [ChromeDriver - WebDriver for Chrome](https://sites.google.com/chromium.org/driver/) to download the corresponding version of ChromeDriver.
   - After downloading, extract the executable file (`chromedriver.exe` on Windows) to a known directory on your system, such as `C:\WebDriver\bin`.

   #### Setting the Chrome WebDriver Path:
   In order for the automation script to interact with the Chrome browser, it is necessary to add the path to the Chrome WebDriver executable to your system's environment variables:

   #### For Windows:
   1. Right-click on 'This PC' or 'Computer' on the desktop or in File Explorer.
   2. Click on 'Properties'.
   3. Select 'Advanced system settings'.
   4. On the System Properties dialog that appears, click on the 'Environment Variables...' button.
   5. Under the 'System variables' section, scroll to find the 'Path' variable and select it.
   6. Click 'Edit...'.
   7. In the 'Edit Environment Variable' dialog, click 'New' and add the path where your ChromeDriver is located, e.g., `C:\WebDriver\bin`.
   8. Click 'OK' to close each of the dialogs.

   #### For macOS/Linux:
   1. Open a terminal window.
   2. Use the `export` command to set the PATH variable:
      ```bash
      export PATH=$PATH:/path/to/directory/containing/chromedriver
      ```
   3. To make this change permanent, add the export command to your shell profile file (e.g., `.bash_profile`, `.zshrc`, `.bashrc`).

   Ensure that the path to `chromedriver` is correct and it matches the location where the executable is stored. Once this step is completed, Selenium WebDriver will be able to use Chrome for automated tasks.

2. ###**Create a New Google Account**: 
Run the `run_webdriver.py` script to initiate an automated Google account creation process:

```bash
python run_webdriver.py
```

Please Note: This script will assist you in creating a new Google account for this project. It is strongly recommended that you only use this account with the WebDriver and not for personal activities, as Google does not allow automated logins for accounts due to security policies. There is a risk associated with creating any account automatically, and by doing so, you acknowledge that you take full responsibility for any repercussions.

3. ###**Configure the WebDriver Account**:
Once your account is created, ensure that you only utilize it within the web driver context to avoid security issues.

4. ###**Update the `config.json` File**

The `config.json` file contains essential configuration details and must be updated with credentials from your newly created Google account, the name of the WhatsApp chat that contains the Google Meet links, and settings for your screen recording software, including executable paths and hotkeys for starting and stopping the recording. This file is located in the `data` directory. If it doesn't exist, create one with the following structure:

```json
{
    "gmail_id": "<Your New Google Account Email>",
    "password": "<New Account Password>",
    "chat_name": "<Name of Your WhatsApp Chat>",
    "recorder": {
        "path": "<Path to Recorder Executable>",
        "start_recording_hotkey": ["<Modifier Key>", "<Key>"],
        "stop_recording_hotkey": ["<Modifier Key>", "<Key>"]
    }
}
```
Replace `<Your New Google Account Email>`, `<New Account Password>`, `<Name of Your WhatsApp Chat>`, `<Path to Recorder Executable>`, `<Modifier Key>`, and `<Key>` with the appropriate details:

- Your New Google Account Email: Email address of the Google account.
- New Account Password: Password of the newly created Google account.
- Name of Your WhatsApp Chat: Name of the WhatsApp chat to scan for Google Meet links.
- Path to Recorder Executable: File path to your screen recording software.
- Modifier Key and Key: Keys used to initiate and end recording.

For example:

```json 
{
"path": "C:\\Program Files (x86)\\Icecream Screen Recorder 7\\recorder.exe",
"start_recording_hotkey": ["ctrl", "r"],
"stop_recording_hotkey": ["ctrl", "s"] 
}
```
In this example, `"C:\\Program Files (x86)\\Icecream Screen Recorder 7\\recorder.exe"` this points to the Icecream Screen Recorder executable.pressing `Ctrl+R` starts the recording and `Ctrl+S` stops it.

5. ###**Meeting Admission Wait Time**: 
To enhance the efficiency and user experience during the admission process to online meetings, our `meeting.py` script offers customizable settings. These settings allow you to define how long the system should wait for a participant's admission and the frequency of admission checks.

You have control over two significant variables within the script:
#### `max_wait_time`
This parameter specifies the maximum duration (in seconds) the system will wait for an attendee to be admitted into a meeting. By default, it is set to `300 seconds` (5 minutes). Increasing this value may be helpful if participants are experiencing longer wait times.

#### `wait_interval`
The interval between each check for meeting admission status (in seconds). By default, the checking interval is every `10 seconds`. Decreasing this time may lead to quicker updates on admission status but might increase the load due to more frequent checks.

#### Applying Configurations: Step-by-Step Instructions

1. **Locate the Script**: Open the `meeting.py` file in your preferred text editor.

2. **Find Configuration Variables**: Search for the `max_wait_time` and `wait_interval` variables within the script.

3. **Edit Values**: Change the values of these variables to match your desired configuration. For example:

    ```python
    max_wait_time = 600  # Sets max wait time to 600 seconds (10 minutes)
    wait_interval = 5    # Sets the check interval to 5 seconds
    ```

4. **Save Changes**: Make sure to save the updated `meeting.py` script after editing.

5. **Run the Script**: Execute the modified script for the new settings to take effect.

By customizing `max_wait_time` and `wait_interval`, you can optimize the admission process according to specific needs or preferences, ensuring a smooth experience for both hosts and attendees of your online meetings.
    
6. ###**Check for UI Changes**: 
If you encounter errors related to finding the XPath or if a UI element is not located, it may be required to review and modify the XPaths used in the configuration. This can be done by running `run_webdriver.py`, logging into the web application, and utilizing developer tools to inspect the elements and extract their XPaths. Make the necessary changes to the `config.json` file to reflect these updates.

## Disclaimer

This project is designed strictly for educational purposes only. By using this software, you agree to do so at your own risk. The author of this project takes no responsibility for the creation of Google accounts nor for the actions taken by users of this script. It is ultimately your responsibility to comply with Google's terms of service and other applicable laws or regulations.

## Usage

Run the main script using the following command:

```bash
python src/main.py
```

When the script is executed, it will prompt you to scan the QR code for WhatsApp Web. Once authenticated, it will monitor the specified chat for any new Google Meet links and proceed with joining the meetings

## Error Handling
The script includes basic error handling for scenarios such as timeouts or unexpected exceptions. It will output informative messages to help diagnose issues.

Example error handling in case of timeouts:

```python
try:
    chat_name = get_chat_name_from_config()  # Fetch the chat name from the config file.
    fetch_meet_link_from_whatsapp(chat_name)  # Use the fetched chat name here.
except TimeoutException as e:
    print("An element could not be located within the specified time:")
    print(e.msg)
```
Remember to handle any potential exceptions resulting from UI changes or incorrect XPath queries. Update the config.json accordingly and ensure correct element identification and interaction.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
    
    A special thanks 
## GurrPratap Sangha my friend who motivated me to do his labour job. 
    And thanks to Selenium WebDriver contributors.

    Gratitude towards the creators of Python and its rich ecosystem of packages.