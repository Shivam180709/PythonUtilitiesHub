# Python 3.12.6  

import re
from time import sleep
import pygame
import threading
import datetime

#Functions for alarm
def extract_alarm_time(user_input):
    # Regex to extract the hour, minute, and AM/PM or a.m./p.m.
    match = re.search(r"(\d{1,2}):(\d{2})\s*(AM|PM|a\.m\.|p\.m\.)", user_input, re.IGNORECASE)
    
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        period = match.group(3).lower()  # Lowercase the period for consistent comparison
        # Convert the period to "am" or "pm" for easier handling
        if period in ['a.m.', 'am']:
            period = "AM"
        elif period in ['p.m.', 'pm']:
            period = "PM"
        # Convert to 24-hour format
        if period == "PM" and hour != 12:
            hour += 12
        elif period == "AM" and hour == 12:
            hour = 0
        # Return a datetime object representing today at the given time
        now = datetime.datetime.now()
        alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        # If the alarm time has already passed today, set it for tomorrow
        if alarm_time < now:
            alarm_time = alarm_time.replace(day=now.day + 1)
        a = f"Alarm set for {alarm_time.strftime('%I:%M %p')}"
        print(a)
        return alarm_time
    return None
def set_alarm(alarm_time):
    def monitor_alarm():
        
        # Continuously check if the alarm time has been reached
        while True:
            current_time = datetime.datetime.now()
            if current_time >= alarm_time:
                print("ALARM! Time's up!")
                
                pygame.mixer.init()
                pygame.mixer.music.load("Alarm_timer_sound.wav")
                sleep(2)
                for i in range(4):
                    pygame.mixer.music.play()
                    sleep(2)
                # You could add sound, a notification, or other alarm actions here
                break
            # Sleep for a minute before checking again to avoid high CPU usage
            sleep(30)
    # Start the monitoring in a separate thread
    alarm_thread = threading.Thread(target=monitor_alarm)
    alarm_thread.start()
def handle_alarm_command(user_input):
    # Extract the alarm time from the user input
    alarm_time = extract_alarm_time(user_input)
    
    if alarm_time is not None:
        # If a valid alarm time is found, set the alarm
        set_alarm(alarm_time)
    else:
        print("Sorry, I couldn't understand the alarm time.")

if "__main__"==__name__:

    # sample input : Set alarm for 8:45 pm.
    # sample input : Set timer for 9:00 am.
    # sample input : Set timer for 12:00 pm.
    user_input = input("Enter The Duration: ") 
    handle_alarm_command(user_input)