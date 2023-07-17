import speech_recognition as sr
import openai
import requests
import io
from pydub import AudioSegment
from pydub.playback import play

# Setting the API keys
openai.api_key = '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'
elevenLabsAPIKey = '00f0c42b5a788b2c432412bc6fc96f02'

# Setting the recognizer and microphone
r = sr.Recognizer()
mic = sr.Microphone()

# Getting the voice from ElevenLabs
response = requests.get('https://api.elevenlabs.io/v1/voices', headers={'xi-api-key': elevenLabsAPIKey})

# Access the first voice's ID
voice_id = response.json()["voices"][0]["voice_id"]  # Assuming the first voice is Jarvis

voices = response.json()["voices"]
voice_id = next((voice["voice_id"] for voice in voices if voice["name"] == "Jarvis"), None)

# Starting the conversation with the AI
conversation = [{"role": "system", "content": "You are Jarvis, Falco's personal assistant."}]

while True:
    # Listening to the user's voice
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = r.listen(source)

    # Recognizing the speech
    speech = r.recognize_google(audio, language='de-DE')
    print(f"Recognized speech: {speech}")

    if "draw" in speech:
        # The user asked the AI to draw something
        start_index = speech.find("draw") + 5
        prompt = speech[start_index:]
        response = openai.Image.create(prompt=prompt, n=1, size="1024x1024")
        image_url = response['data'][0]['url']
        print(f"Drawing prompt: {prompt}")
        print(f"Image URL: {image_url}")

    else:
        # The user is conversing with the AI
        conversation.append({"role": "user", "content": speech})
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation)
        message = response["choices"][0]["message"]["content"]
        conversation.append({"role": "assistant", "content": message})

        # Converting the AI's response to speech
        response = requests.post(
            f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream',
            headers={'xi-api-key': elevenLabsAPIKey},
            json={'text': message, 'model_id': 'eleven_multilingual_v1'}
        )
        audio = io.BytesIO(response.content)
        sound = AudioSegment.from_file(audio, format="mp3")
        play(sound)