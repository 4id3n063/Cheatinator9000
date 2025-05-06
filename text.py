import pyttsx3
import os
from groq import Groq
from dotenv import load_dotenv
import sounddevice as sd
from scipy.io.wavfile import write
import random

# Load environment variables
load_dotenv()

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize Groq client
client = Groq(api_key=os.environ.get("API_KEY"))


def memory_read(filename="memorysad.txt"):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return f.read()
    return "(no memory yet)"

def memory(data, filename="memorysad.txt"):
    one_line = data.replace('\n', ' ').strip()
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'a') as f:
        f.write(one_line + "\n")
        

def do_a_mario(prompt):
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "you are a question answering ai. keep your answers short." + "this is what aiden said:" + prompt + memory_read()
            }
        ],
        model="llama3-8b-8192",
    )
    return completion.choices[0].message.content
def random_result():
    number = random.randint(1, 10)
    if 1 <= number <= 8:
        return "User:"
    elif number == 9 or number == 10:
        return "PLEASE HELP ME:"

def BravoVince():
    global UserInput
    print(random_result(), end=" ")
    UserInput = input("").strip().lower()

    do_a_mario(UserInput)

BravoVince()
while True:
    print(f"You said: {UserInput}")

    ai_response = do_a_mario(UserInput)
    ## only for use when no audio driver
    ##engine.save_to_file(ai_response, 'output.mp3')
    print(f"AI: {ai_response}")

    memory(f"user: {UserInput} ai: {ai_response}")


    engine.say(ai_response)
    engine.runAndWait()
    BravoVince()

