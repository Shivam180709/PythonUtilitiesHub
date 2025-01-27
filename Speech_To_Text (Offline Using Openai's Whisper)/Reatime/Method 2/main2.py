# Python 3.12.6

import pyaudio
import wave
import whisper
import tempfile
import os

# Load the Whisper model
model = whisper.load_model("base")

# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5  # Duration to record

def transcribe_audio():
    """
    Records audio from the microphone, saves it temporarily, transcribes it using the Whisper model, 
    and prints the transcription.

    Steps:
    - Records 5 seconds of audio input using PyAudio.
    - Saves the recorded audio to a temporary WAV file.
    - Transcribes the audio using the Whisper model.
    - Prints the transcription to the console.
    - Deletes the temporary audio file after transcription.
    """
    audio = pyaudio.PyAudio()

    # Start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording...")

    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        wf = wave.open(temp_audio_file.name, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        # Transcribe the audio file
        result = model.transcribe(temp_audio_file.name)
        print("Transcription:", result["text"])

    # Remove the temporary file
    os.remove(temp_audio_file.name)

if __name__ == "__main__":
    transcribe_audio()
