import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask 
from pymongo import MongoClient

from .events import socketio
from .routes import main 
from .mandlebrot import mandle
from .oauth2 import oauth

db = MongoClient(os.environ['MONGO_CONNECTION_STRING'])
database = db.get_database(os.environ['MONGO_DATABASE_NAME'])

def create_app():
    app = Flask(__name__)

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
    app.register_blueprint(mandle, url_prefix='/mandlebrot')
    app.register_blueprint(oauth)

    socketio.init_app(app)

    return app