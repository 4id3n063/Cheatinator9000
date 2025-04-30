import pyttsx3
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
engine = pyttsx3.init()
client = Groq(
    api_key = os.environ.get('API_KEY'),  # This is the default and can be omitted
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "what is 2+2, go into extreme detail.",
        }
    ],
    model="llama3-8b-8192",
)
print(chat_completion.choices[0].message.content)
engine.say(chat_completion.choices[0].message.content)
engine.runAndWait()