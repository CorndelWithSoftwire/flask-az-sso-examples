import os
from flask import Flask, redirect, request
from flask_login import login_required, LoginManager, login_user
import requests

from src.user import User

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    url = get_auth_url()
    return redirect(url)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/login/azure/authorized")
def authorised():
    code = request.args.get('code')
    token = get_token_from_code(code)
    user_id = get_user_id(token)
    login_user(User(user_id))
    return redirect("/")

@app.route("/")
@login_required
def index():
    return "This is restricted content!"

def get_auth_url():
    return f'https://login.microsoftonline.com/{os.getenv("AZ_TENANT_ID")}/oauth2/v2.0/authorize?'\
        + f'client_id={os.getenv("AZ_CLIENT_ID")}' \
        + f'&scope={os.getenv("AZ_API_SCOPE")}' \
        + '&response_type=code'

def get_token_from_code(code):
    url = f'https://login.microsoftonline.com/{os.getenv("AZ_TENANT_ID")}/oauth2/v2.0/token'
    data = {
        'client_id': os.getenv('AZ_CLIENT_ID'),
        'client_secret': os.getenv('AZ_CLIENT_SECRET'),
        'scope': 'https://graph.microsoft.com/User.Read',
        'grant_type': 'authorization_code',
        'code': code
    }
    result = requests.post(url, data = data)
    result.raise_for_status()
    token = result.json()['access_token']
    return token

def get_user_id(token):
    user_url = 'https://graph.microsoft.com/v1.0/me/'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    result = requests.get(user_url, headers = headers)
    result.raise_for_status()
    
    json_result = result.json()
    # Result also contains fields such as "displayName" and "mail" (email address)
    id = json_result['id']
    return id