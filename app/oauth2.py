from flask import request, current_app, session, url_for, redirect, g, Blueprint, render_template

import requests
from functools import wraps
from urllib.parse import urlencode


oauth = Blueprint("oauth", __name__)

@oauth.get("/login")
def home():
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

    # print(response.json(), flush=True)
    # print(f'Email {email}', flush=True)

    return render_template("login.html")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
