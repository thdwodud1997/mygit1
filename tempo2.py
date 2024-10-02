import sounddevice as sd
import numpy as np
import librosa
import time

# Parameters
sample_rate = 22050  # Sample rate for librosa
chunk_duration = 2.0  # Process 2-second chunks
chunk_size = int(sample_rate * chunk_duration)
hop_length = 512

# Global buffer for audio data
audio_buffer = np.zeros(chunk_size)

def callback(indata, frames, time, status):
    global audio_buffer
    
    # Reshape the input data into a single array and store in buffer
    audio_buffer[:] = np.roll(audio_buffer, -frames)
    audio_buffer[-frames:] = indata[:, 0]

def detect_and_follow_beats():
    try:
        # Perform tempo detection and get beat frames
        tempo, beat_frames = librosa.beat.beat_track(y=audio_buffer, sr=sample_rate)
        
        # Convert beat frames to time in seconds
        beat_times = librosa.frames_to_time(beat_frames, sr=sample_rate, hop_length=hop_length)
        
        # Get the start time to synchronize with real time
        start_time = time.time()
        
        # Follow the beat and print "doom"
        for beat_time in beat_times:
            while time.time() - start_time < beat_time:
                pass  # Wait until the actual beat time
            print("doom")
        
    except Exception as e:
        print(f"Error in beat following: {e}")

# Start audio stream
stream = sd.InputStream(callback=callback, channels=1, samplerate=sample_rate, blocksize=chunk_size)
stream.start()

print("Listening and following beats...")

try:
    while True:
        detect_and_follow_beats()
        sd.sleep(int(chunk_duration * 1000))  # Sleep for the duration of chunk
except KeyboardInterrupt:
    print("Stopping...")
    stream.stop()
    stream.close()
