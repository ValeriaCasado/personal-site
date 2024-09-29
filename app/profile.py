from flask import Blueprint, render_template
from flask_login import login_required


user_profile = Blueprint("profile", __name__)

@login_required
@user_profile.get("/")
def get_profile():
    return render_template("profile.html")