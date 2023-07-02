from flask import Flask
from flask_cors import CORS
from app.decryptor import Decryptor

app = Flask(__name__)
CORS(app)
dec = Decryptor()

from app import routes
