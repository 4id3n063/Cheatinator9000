import pyttsx3
import os
from groq import Groq
from dotenv import load_dotenv
import json
import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(filename="recording.wav", duration=5, fs=48000, channels=2):
    print("🎙️ Recording started...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=channels, dtype='int16')
    sd.wait()
    write(filename, fs, audio)
    print(f"✅ Recording saved to {filename}")

def transcribe():
    filename = os.path.join(os.path.dirname(__file__), "recording.wav")
    record_audio(filename, duration=5)

    client = Groq(api_key=os.environ.get('API_KEY'))

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

        # Extract the "text" field from the transcription
        transcription_text = transcription.model_dump()["text"]
        print(f"Transcription Text: {transcription_text}")
        return transcription_text

# Load environment variables
load_dotenv()

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize Groq client
client = Groq(
    api_key=os.environ.get('API_KEY')  # Removed the extra comma
)

# Transcribe audio and use the result as the prompt
text = transcribe()

# Generate chat completion
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": text + "your responses should be short. don't use asteriks unless it's required."
        }
    ],
    model="llama3-8b-8192",
)

# Output and speak the response
response = chat_completion.choices[0].message.content
print(response)
engine.say(response)
engine.runAndWait()