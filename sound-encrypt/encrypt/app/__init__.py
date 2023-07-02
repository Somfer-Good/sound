from flask import Flask
from flask_cors import CORS
from app.encyptor import Encryptor

app = Flask(__name__)
CORS(app)
enc = Encryptor()

from app import routes
