import base64
from app import app, enc
from app.encyptor import UnidentifiedChar
from flask import request, send_file, Response
import wave

@app.post('/encrypt')
def encrypt():
    try:
        enc.encrypt(request.get_json()['text'])
    except UnidentifiedChar:
        return '', 500
    else:
        return base64.b64encode(open('морзе.wav', 'rb').read())

