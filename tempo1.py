import sounddevice as sd
import numpy as np
import librosa

# Parameters
sample_rate = 22050  # Sample rate for librosa
chunk_duration = 2.0  # Process 2-second chunks
chunk_size = int(sample_rate * chunk_duration)

# Global buffer for audio data
audio_buffer = np.zeros(chunk_size)

def callback(indata, frames, time, status):
    global audio_buffer
    
    # Reshape the input data into a single array and store in buffer
    audio_buffer[:] = np.roll(audio_buffer, -frames)
    audio_buffer[-frames:] = indata[:, 0]

def detect_tempo():
    # Perform tempo detection on the current audio buffer
    try:
        tempo, _ = librosa.beat.beat_track(y=audio_buffer, sr=sample_rate)
        #print(librosa.beat.beat_track(y=audio_buffer, sr=sample_rate))
        print(f"Detected Tempo: {tempo[0]:.2f} BPM")
    except Exception as e:
        print(f"Error in tempo detection: {e}")

# Start audio stream
stream = sd.InputStream(callback=callback, channels=1, samplerate=sample_rate, blocksize=chunk_size)
stream.start()

print("Listening...")

try:
    while True:
        detect_tempo()
        sd.sleep(int(chunk_duration * 1000))  # Sleep for the duration of chunk
except KeyboardInterrupt:
    print("Stopping...")
    stream.stop()
    stream.close()
