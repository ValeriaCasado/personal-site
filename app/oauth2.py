from flask import request, current_app, flash, url_for, redirect, g, Blueprint, render_template
from flask_login import login_user, login_required, logout_user
import requests
from functools import wraps
from urllib.parse import urlencode

from .models import User
from . import login_manager

oauth = Blueprint("oauth", __name__)

@oauth.get("/login")
def login():
    return render_template("login.html")


@oauth.get("/authenticate/<provider>")
def authorize(provider):

    print(f'{provider}', flush=True)

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)

    # create a query string with all the OAuth2 parameters
    # https://developers.google.com/identity/protocols/oauth2/web-server#python
    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('oauth.callback', provider=provider, _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        # 'state': session['oauth2_state'],
    })

    current_app.logger.info(f"REDIRECT URL: {url_for('oauth.callback', provider=provider, _external=True)}")
    print(provider_data['client_id'], flush=True)
    print(provider_data['authorize_url'] + '?' + qs, flush=True)

    return redirect(provider_data['authorize_url'] + '?' + qs)


@oauth.get("/callback/<provider>")
def callback(provider):

    # Get the authorisation code 
    authorization_code = request.args['code']

    print(f'Authorization code: ' + authorization_code)

    # Provider details
    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)

    # Exchange the authorization code for an access token
    response = requests.post(provider_data['token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('oauth.callback', provider=provider, _external=True),
    }, headers={'Accept': 'application/json'})

    oauth2_token = response.json().get('access_token')
    if not oauth2_token:
        print(response.json())
        current_app.logger.error(response.json())

    print(f'Request token: ' + oauth2_token)
    
    # use the access token to get the user's email address
    response = requests.get(provider_data['userinfo']['url'], headers={
        'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    })

    d = response.json()
    print(d, flush=True)


    user = User.load_user(d['email'])
    if not user:
        user = User(
            email=d['email'],
            sub=d['sub'],
            given_name=d['given_name'],
            family_name=d['family_name'],
            picture=str(d['picture'])
        ).save()

    login_user(user)
    flash('Logged in successfully.')
    
    return redirect(url_for('profile.get_profile'))


@oauth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out.')
    return redirect(url_for('main.home'))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@login_manager.user_loader
def load_user(user_id):
    return User.load_user(user_id)