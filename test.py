import os
import json
from groq import Groq
import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(filename="recording.wav", duration=5, fs=44100):
    print("🎙️ Recording started...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    write(filename, fs, audio)
    print(f"✅ Recording saved to {filename}")

def transcribe():
    # Step 1: Record audio
    filename = os.path.join(os.path.dirname(__file__), "recording.wav")
    record_audio(filename, duration=5)

# Step 2: Initialize the Groq client
    client = Groq(api_key=os.environ.get('API_KEY'))

# Step 3: Open and send the audio file
    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=file,
            model="whisper-large-v3-turbo",
            prompt="Specify context or spelling",
            response_format="verbose_json",
            timestamp_granularities=["word", "segment"],
            language="en",
            temperature=0.0
        )
        # Step 4: Display full result
        print(json.dumps(transcription.model_dump(), indent=2))

transcribe()
