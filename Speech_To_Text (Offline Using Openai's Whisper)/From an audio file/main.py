import whisper

# Load the Whisper model
model = whisper.load_model("base")

# Load and transcribe the audio file
result = model.transcribe("From an audio file/sample.mp3")

# Print the transcribed text
print(result["text"])
