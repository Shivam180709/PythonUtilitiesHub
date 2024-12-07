# Python 3.12.6
import pyaudio  # Library for accessing audio input and output devices
import struct  # For unpacking binary data
import math  # For mathematical calculations
import os  # For interacting with the operating system (not used in this code)

# Constants for configuration
INITIAL_TAP_THRESHOLD = 0.02  # Initial threshold for detecting claps
FORMAT = pyaudio.paInt16  # Format for 16-bit audio
SHORT_NORMALIZE = (1.0 / 32768.0)  # Normalization factor for audio samples
CHANNELS = 2  # Number of audio channels (stereo)
RATE = 44100  # Sampling rate in Hz
INPUT_BLOCK_TIME = 0.05  # Duration of each audio block in seconds
INPUT_FRAMES_PER_BLOCK = int(RATE * INPUT_BLOCK_TIME)  # Number of frames per block
OVERSENSITIVE = 15.0 / INPUT_BLOCK_TIME  # Sensitivity adjustment for noisy environments
UNDERSENSITIVE = 120.0 / INPUT_BLOCK_TIME  # Sensitivity adjustment for quiet environments
MAX_TAP_BLOCKS = 0.15 / INPUT_BLOCK_TIME  # Max blocks of continuous noise treated as a single clap

# Function to calculate the Root Mean Square (RMS) of audio samples
def get_rms(block):
    """
    Calculate the Root Mean Square (RMS) of a block of audio samples.
    Args:
        block (bytes): Raw audio data.
    Returns:
        float: RMS value representing the average amplitude.
    """
    count = len(block) / 2  # Each sample is 2 bytes
    format = "%dh" % count  # Format string for unpacking the binary data
    shorts = struct.unpack(format, block)  # Unpack the binary data into integers
    sum_squares = 0.0  # Sum of squares of normalized samples

    for sample in shorts:
        n = sample * SHORT_NORMALIZE  # Normalize the sample
        sum_squares += n * n  # Square and accumulate

    return math.sqrt(sum_squares / count)  # Return the square root of the mean

# Class for detecting claps using microphone input
class TapTester(object):

    def __init__(self):
        """
        Initialize the TapTester instance.
        """
        self.pa = pyaudio.PyAudio()  # Initialize PyAudio
        self.stream = self.open_mic_stream()  # Open the microphone stream
        self.tap_threshold = INITIAL_TAP_THRESHOLD  # Set the initial threshold
        self.noisycount = MAX_TAP_BLOCKS + 1  # Initialize noise counter
        self.quietcount = 0  # Counter for quiet periods
        self.errorcount = 0  # Counter for errors

    def stop(self):
        """
        Stop the microphone stream.
        """
        self.stream.close()

    def find_input_device(self):
        """
        Find the index of an input device (microphone).
        Returns:
            int: Index of the input device, or None if not found.
        """
        device_index = None  # Default to None

        # Iterate over available devices
        for i in range(self.pa.get_device_count()):
            devinfo = self.pa.get_device_info_by_index(i)  # Get device info

            # Look for keywords in the device name
            for keyword in ["mic", "input"]:
                if keyword in devinfo["name"].lower():
                    device_index = i  # Found a matching device
                    return device_index

        # If no preferred device is found, use the default
        if device_index is None:
            print("No preferred input found; using default input device.")

        return device_index

    def open_mic_stream(self):
        """
        Open the microphone input stream.
        Returns:
            stream: PyAudio stream object.
        """
        device_index = self.find_input_device()  # Get the device index

        # Open the audio stream
        stream = self.pa.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=INPUT_FRAMES_PER_BLOCK
        )
        return stream

    def listen(self):
        """
        Listen to the audio input and process sound levels.
        Returns:
            str: "True-Mic" if a clap is detected, else None.
        """
        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK)  # Read a block of audio
        except IOError as e:
            self.errorcount += 1  # Increment error counter
            print(f"({self.errorcount}) Error recording: {e}")
            self.noisycount = 1  # Reset noise counter
            return

        amplitude = get_rms(block)  # Calculate the RMS amplitude

        # Check if the amplitude exceeds the threshold
        if amplitude > self.tap_threshold:
            self.quietcount = 0  # Reset quiet counter
            self.noisycount += 1  # Increment noisy counter

            # Adjust the threshold if too sensitive
            if self.noisycount > OVERSENSITIVE:
                self.tap_threshold *= 1.1
        else:
            # Check for a valid clap
            if 1 <= self.noisycount <= MAX_TAP_BLOCKS:
                return "True-Mic"

            self.noisycount = 0  # Reset noisy counter
            self.quietcount += 1  # Increment quiet counter

            # Adjust threshold if too insensitive
            if self.quietcount > UNDERSENSITIVE:
                self.tap_threshold *= 2

# Main function to detect claps
def Tester():
    """
    Main function to initialize the TapTester and detect claps.
    """
    tt = TapTester()  # Create an instance of TapTester

    while True:
        kk = tt.listen()  # Listen for claps

        if "True-Mic" == kk:
            print("\n\n> Clap Detected\n")
            return "True-Mic"

# Entry point
if __name__ == "__main__":
    Tester()
