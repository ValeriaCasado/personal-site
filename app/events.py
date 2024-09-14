from flask import request
from flask_socketio import emit
import numpy as np
from .mandlebrot import get_new_range, mandlebrot

from .extensions import socketio

DENSITY = 1000

users = {}

# @socketio.on("connect")
# def handle_connect():
#     print("Client connected!")

@socketio.on("user_join")
def handle_user_join(username):
    print(f"User {username} joined!")
    users[username] = request.sid

@socketio.on("new_message")
def handle_new_message(message):
    print(f"New message: {message}")
    username = None 
    for user in users:
        if users[user] == request.sid:
            username = user
    emit("chat", {"message": message, "username": username}, broadcast=True)


@socketio.on("new_mandlebrot")
def draw_mandlebrot(info = {}):
    coordinates = info.get('coordinates')
    real_range = info['range']['real'] if info.get('range') else None
    imaginary_range = info['range']['imaginary'] if info.get('range') else None
    threshold = info.get('threshold', 100)

    real_range, imaginary_range = get_new_range(
        real_range=real_range,
        imaginary_range=imaginary_range,
        coord=coordinates,
        density=1000
    )

    emit("set_range", {
        'real': real_range,
        'imaginary': imaginary_range
    })

    # Create new mandlebrot in new coord space
    mandlebrot(
        real_range=real_range,
        imaginary_range=imaginary_range,
        threshold=threshold,
        density=1000,
        emit_function=lambda data: emit("draw_row", data)
    )