# Python 3.12.6

import speech_recognition as sr
import whisper

# Initialize microphone, recognizer, and Whisper model
source = sr.Microphone()
recognizer = sr.Recognizer()
base_model = whisper.load_model('base')

def listen_for_command():
    """
    Listens for voice input, saves it as a WAV file, and transcribes the audio using the Whisper model.

    Returns:
        str: The transcribed text in lowercase if successful, otherwise None.
    """
    with source as s:
        print("Listening for commands...")
        # Adjust microphone for ambient noise
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Save the audio data to a file
        with open("command.wav", "wb") as f:
            f.write(audio.get_wav_data())
        
        # Transcribe the audio using Whisper
        command = base_model.transcribe("command.wav")
        
        # Return the text from the transcription if available
        if command and command['text']:
            return command['text'].lower()
        return None
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError:
        print("Unable to access the Google Speech Recognition API.")
        return None


if __name__ == "__main__":
    # Run the function and print the result
    print(listen_for_command())
