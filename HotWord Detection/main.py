# Python 3.12.6
import threading
import speech_recognition as sr

# Create a recognizer object
recognizer = sr.Recognizer()
hotword = 'shivam'

def listen():
    """
    Continuously listens for user speech from the microphone.
    
    The function listens for audio input in an infinite loop and processes 
    it using a separate thread to ensure non-blocking behavior.
    """
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            
            # Send audio for processing in a new thread
            threading.Thread(target=process_audio, args=(audio,)).start()

def process_audio(audio):
    """
    Processes the captured audio and converts it into text.
    
    Args:
        audio (AudioData): The audio data to be processed.
    
    If the audio contains the defined hotword, it triggers a specific action.
    Catches exceptions for unrecognized speech or API request errors.
    """
    try:
        print("Processing audio...")
        # Recognize speech using Google Web Speech API
        text = recognizer.recognize_google(audio, language='en-IN')
        print(f"Recognized: {text}")
        
        # Check if the hotword is present in the recognized text
        if hotword in text.lower():
            # Action to take when hotword is detected
            print("ACTIVATING >>>>..........")
    
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Request error from Google Speech Recognition service: {e}")

if __name__ == "__main__":
    """
    Main entry point of the program.
    
    Starts the listening thread to capture user speech and process it 
    asynchronously in separate threads.
    """
    # Start the listening thread
    listening_thread = threading.Thread(target=listen)
    listening_thread.start()
