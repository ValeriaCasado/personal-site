import os

from flask import Flask 
from pymongo import MongoClient

from .events import socketio
from .routes import main 
from .mandlebrot import mandle

db = MongoClient(os.environ['MONGO_CONNECTION_STRING'])

def create_app():
    app = Flask(__name__)


    app.config['MONGODB_SETTINGS'] = {
        "db": "myapp",
    }

    app.register_blueprint(main)
    app.register_blueprint(mandle, url_prefix='/mandlebrot')

    socketio.init_app(app)

    return app