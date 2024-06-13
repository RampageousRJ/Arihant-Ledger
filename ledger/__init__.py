from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('LEDGER_SECRET_KEY')
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('LEDGER_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('LEDGER_PRIVATE_KEY')

import ledger.routes