# Python 3.12.6  

import re
from time import sleep
import pygame
import threading


# Function for Timmer 
def extract_time(user_input):
# Regex to find the number and unit (minutes, seconds, hours)
    match = re.search(r"(\d+)\s*(seconds?|minutes?|hours?)", user_input.lower())    
    if match:
        time_value = int(match.group(1))  # Extract the number (e.g., 5)
        time_unit = match.group(2)        # Extract the time unit (e.g., minutes)   
        # Convert everything to seconds for simplicity
        if "second" in time_unit:
            return time_value
        elif "minute" in time_unit:
            return time_value * 60
        elif "hour" in time_unit:
            return time_value * 3600
    return None  # Return None if no valid time is found        
def set_timer(duration_seconds):
    def countdown():
        sleep(duration_seconds)  # Wait for the specified time
        print("Timer! Time UP.")
        pygame.mixer.init()
        pygame.mixer.music.load("Alarm_timer_sound.wav")
        sleep(2)
        for i in range(4):
            pygame.mixer.music.play()
            sleep(2)
    
    # Start a new thread to run the countdown timer
    timer_thread = threading.Thread(target=countdown)
    timer_thread.start()
def handle_timer_command(user_input):
    # Extract the time from the user input
    duration_seconds = extract_time(user_input)
    
    if duration_seconds is not None:
        # If valid time is found, set the timer
        set_timer(duration_seconds)
        mgs = f"Timer started for {duration_seconds} seconds."
        print(mgs)
    else:
        # If no valid time is found in the input
        print("Sorry, I couldn't understand the time duration.")

if "__main__"==__name__:

    # sample input : Set timer for 4 seconds.
    # sample input : Set timer for 5 minutes.
    # sample input : Set timer for 1 hour.
    user_input = input("Enter The Duration: ") 
    handle_timer_command(user_input)