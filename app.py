import os
import speech_recognition as sr
import openai
import requests
import io
from pydantic import BaseModel
from typing import Optional
from pydub import AudioSegment
from pydub.playback import play
import dotenv
from fastapi import FastAPI
from twilio.twiml.voice_response import VoiceResponse
from fastapi import Request



# Load environment variables
dotenv.load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
elevenLabsAPIKey = os.getenv('ELEVENLABS_VARIABLE')

app = FastAPI()

@app.post("/voice")
async def voice():
    response = VoiceResponse()
    response.say("Hello")
    return str(response)


@app.post("/gather")
async def handle_gather(request: Request):
    data = await request.form()
    data_dict = dict(data)
    print(data_dict)

    recording_url = data_dict.get("RecordingUrl")
    print("Recording URL:", recording_url)

    if recording_url is None:
        response = VoiceResponse()
        response.say("Sorry, there was an issue with the recording. Please try again.")
        return str(response)

    response = get_response_from_ai(recording_url)

    twiml_response = VoiceResponse()
    twiml_response.say("Responding. Please wait.")  # Indicate that the program is responding

    if response is not None:
        twiml_response.say(response)  # Play the AI's response
    else:
        twiml_response.say("Sorry, I couldn't process your request.")

    return str(twiml_response)


def get_response_from_ai(recording_url):
    # Use your AI model or API to generate a response based on the recording URL
    # Replace this with your actual code
    try:
        audio = get_audio_from_url(recording_url)
        r = sr.Recognizer()
        audio_data = sr.AudioData(audio, 16000, 2)
        speech = r.recognize_google(audio_data)
        print("User input:", speech)
        return "This is your AI-generated response"
    except Exception as e:
        print("Error:", str(e))
        return None


def get_audio_from_url(url):
    response = requests.get(url)
    audio = io.BytesIO(response.content)
    sound = AudioSegment.from_file(audio, format="mp3")
    return sound.raw_data


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)