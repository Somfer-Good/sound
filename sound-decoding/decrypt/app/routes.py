from app import app, dec
from app.decryptor import UnidentifiedChar
from flask import request, jsonify

@app.post('/decrypt')
def index():
    try:
        result = dec.decrypt(request.get_json()['wav'])
    except UnidentifiedChar:
        return '', 500
    else:
        return jsonify(
            {
                "text" : result
            }
        )

