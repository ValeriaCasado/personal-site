import os
import certifi

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, session
from flask_login import LoginManager
from pymongo import MongoClient
from datetime import timedelta

ca = certifi.where()
db = MongoClient(os.environ['MONGO_CONNECTION_STRING'], tlsCAFile=ca)
database = db.get_database(os.environ['MONGO_DATABASE_NAME'])
login_manager = LoginManager()

from .models import *
from .events import socketio
from .routes import main 
from .mandlebrot import mandle
from .oauth2 import oauth
from .profile import user_profile


def create_app():
    app = Flask(__name__)


    app.config['USE_PERMANENT_SESSION'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
    app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']


    app.config['OAUTH2_PROVIDERS'] = {

    # Google OAuth 2.0 documentation:
    # https://developers.google.com/identity/protocols/oauth2/web-server#httprest
    'google': {
        'client_id': os.environ['GOOGLE_CLIENT_ID'],
        'client_secret': os.environ['GOOGLE_CLIENT_SECRET'],
        'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
        'token_url': 'https://accounts.google.com/o/oauth2/token',
        'userinfo': {
            'url': 'https://www.googleapis.com/oauth2/v3/userinfo'
        },
        'scopes': [
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile'],
        }
    }


    app.register_blueprint(main)
    app.register_blueprint(oauth)
    app.register_blueprint(mandle, url_prefix='/mandlebrot')
    app.register_blueprint(user_profile, url_prefix='/profile')

    socketio.init_app(app)
    
    login_manager.init_app(app)

    return app