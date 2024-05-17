from naoqi import ALProxy
import numpy as np

# Replace 'robot_ip' and '9559' with your robot's IP address and port
robot_ip = "192.168.1.140"
robot_port = 9559

# Connect to ALSoundProcessing and ALAudioDevice proxies
sound_processing = ALProxy("ALSoundProcessing", robot_ip, robot_port)
audio_device = ALProxy("ALAudioDevice", robot_ip, robot_port)

# Define a callback to process audio data
def audio_callback(nb_of_channels, nb_of_samples_by_channel, time_stamp, input_buffer):
    # Convert the input buffer to a numpy array
    audio_data = np.frombuffer(input_buffer, dtype=np.int16).reshape(nb_of_samples_by_channel, nb_of_channels)

    # Calculate the RMS (Root Mean Square) value for each microphone to get the audio level
    rms_values = np.sqrt(np.mean(audio_data**2, axis=0))

    # Print or log the RMS values for each microphone
    for i in range(nb_of_channels):
        print(f"Microphone {i} RMS: {rms_values[i]}")

# Subscribe to ALSoundProcessing to get audio data
sound_processing.subscribe("TestMicrophones")

# Register the callback
audio_device.setClientPreferences("TestMicrophones", 16000, 0, 0)
audio_device.subscribe("TestMicrophones", "python_callback", audio_callback)

# Allow some time for audio data to be processed
import time
time.sleep(10)

# Unsubscribe from ALSoundProcessing
sound_processing.unsubscribe("TestMicrophones")

# Clean up
audio_device.unsubscribe("TestMicrophones")

print("Finished microphone test.")
