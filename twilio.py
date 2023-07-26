from fastapi import FastAPI, Request, HTTPException
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client

app = FastAPI()

account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
twilio_phone_number = 'your_twilio_phone_number'
your_phone_number = 'your_phone_number'


@app.post('/call')
async def initiate_call(request: Request):
    response = VoiceResponse()
    response.say('Hi!')
    return str(response)


@app.post('/start')
async def start_call(request: Request):
    client = Client(account_sid, auth_token)
    call = client.calls.create(
        url=request.url_for('initiate_call'),
        to=your_phone_number,
        from_=twilio_phone_number
    )
    return str(call.sid)