from functools import wraps
import os
from flask import Flask, redirect, request, session, url_for
from flask_login import current_user, login_required, LoginManager, login_user
from msal import ConfidentialClientApplication

from src.user import User

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
client = ConfidentialClientApplication(
    client_id = os.getenv("AZ_CLIENT_ID"),
    client_credential = os.getenv("AZ_CLIENT_SECRET"),
    authority = f'https://login.microsoftonline.com/{os.getenv("AZ_TENANT_ID")}'
)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    flow = client.initiate_auth_code_flow(
        scopes=[os.getenv('AZ_API_SCOPE')]
    )
    session["flow"] = flow
    return redirect(flow["auth_uri"])

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/login/azure/authorized")
def authorised():
    result = client.acquire_token_by_auth_code_flow(session["flow"], request.args)
    # Optionally claim the token yourself:
    # token = result["access_token"]
    user_details = result.get("id_token_claims")
    user_id = user_details['preferred_username']
    login_user(User(user_id))
    return redirect("/")

@app.route("/")
@login_required
def index():
    return f"This is restricted content, {current_user.id}!"