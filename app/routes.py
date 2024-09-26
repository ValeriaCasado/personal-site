from flask import Blueprint, render_template
from flask import request

main = Blueprint("main", __name__)

@main.get("/")
def home():
    return render_template("index.html")


@main.get("/test")
def test():
    print(request.json)
