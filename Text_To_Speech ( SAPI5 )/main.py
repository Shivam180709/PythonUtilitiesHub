# Python 3.12.6

import pyttsx3

# Initialize the pyttsx3 engine for text-to-speech conversion
engine = pyttsx3.init("sapi5")

# Get available voices and set the desired voice (male or female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Selects the second voice in the list (female in most cases)

# Set the speech rate (words per minute)
engine.setProperty('rate', 170)  # Speed of speech, adjust as needed

def Speak(Text):
    """
    Converts the given text to speech and plays it through the speakers.
    
    Args:
        Text (str): The text string that needs to be spoken.
    """
    engine.say(Text)      # Converts the text to speech
    engine.runAndWait()   # Waits until the speech is finished

if __name__ == "__main__":
    """
    Main entry point of the program.
    
    Calls the Speak function to say the phrase 'Hello from a computer program!' 
    when the program is run.
    """
    Speak("Hello from a computer program!")
