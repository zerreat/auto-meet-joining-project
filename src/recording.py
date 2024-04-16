import time
import subprocess
import pyautogui
import os
from utils import activate_meet_window_by_click, load_config

# Load the settings from the config.json
config = load_config(r'data\config.json')

# Extract settings
path_to_recorder = config['recorder']['path']
start_recording_hotkey = config['recorder']['start_recording_hotkey']
stop_recording_hotkey = config['recorder']['stop_recording_hotkey']


# Define recording functions here
def start_recording():
    try:
        # This line is a brief pause to ensure that the Chrome window has time to become the active window.
        time.sleep(2)

        # The absolute path to the Icecream Screen Recorder executable is set here.
        if not os.path.isfile(path_to_recorder):
            raise FileNotFoundError(f"The path to the recorder is invalid: {path_to_recorder}")

        # Launch the screen recorder application as a separate process without blocking the script's execution.
        subprocess.Popen([path_to_recorder])

        # A delay to give the recorder enough time to initialize and be ready for commands.
        time.sleep(5)

        # PyAutoGUI library is used to simulate keyboard shortcuts; 'Ctrl + R' is the shortcut to start recording.
        pyautogui.hotkey(*start_recording_hotkey)

        # The function from 'utils' attempts to find and activate the Google Meet window where the recording should take place.
        # If it fails to do so, the function returns early and no further actions are taken.
        if not activate_meet_window_by_click():
            return  # If activation of the Meet window fails, exit the function.

        # Additional delay to ensure the recording has started before continuing with other actions.
        time.sleep(5)

        # This appears to be an extraneous repeat of the 'start recording' hotkey sequence and may not be necessary.
        # It is advised to check the necessity of this repetition in the code logic.
        pyautogui.hotkey(*start_recording_hotkey)       
    
    except FileNotFoundError as e:
        # When Icecream Screen Recorder executable is not found, this block catches the error and prints a user-friendly message.
        print(f"Failed to start the recording: {e}")
    except Exception as e:
        # This block catches any unexpected errors that might occur and prints an error message, which can help in debugging.
        print(f"An unexpected error occurred: {e}")

def stop_recording():
    try:
        # Use PyAutoGUI to press the hotkey combination 'Ctrl + S' to stop recording.
        pyautogui.hotkey(*stop_recording_hotkey)
    except Exception as e:
        # Catch any general exceptions that may occur when trying to stop the recording and print an error message for debugging purposes.
        print(f"An error occurred while attempting to stop the recording: {e}")
