from flask import Flask
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)

secret_key = os.environ.get('FLASK_SECRET_KEY')

if secret_key is None:
    raise RuntimeError('Secret Key is not set. \nPlease set a secret key under environment variable named \'FLASK_SECRET_KEY\'.')

app.config['SECRET_KEY'] = secret_key

bcrypt = Bcrypt(app)

from billing_system import routes

