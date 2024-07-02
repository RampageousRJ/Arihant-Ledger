from flask import Flask
import os
from flask_pymongo import PyMongo
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['SECRET_KEY'] = os.getenv('LEDGER_SECRET_KEY')
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('LEDGER_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('LEDGER_PRIVATE_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = 3600

mongo = PyMongo(app)

import ledger.routes