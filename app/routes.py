from flask import Blueprint, render_template
from flask import request
import requests
main = Blueprint("main", __name__)

@main.get("/")
def home():
    return render_template("index.html")