import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.azure import make_azure_blueprint, azure

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
blueprint = make_azure_blueprint(
    client_id=os.getenv("AZ_CLIENT_ID"),
    client_secret=os.getenv("AZ_CLIENT_SECRET"),
    tenant=os.getenv("AZ_TENANT_ID")
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
def index():
    if not azure.authorized:
        return redirect(url_for("azure.login"))
    resp = azure.get("/v1.0/me")
    assert resp.ok
    return "You are {mail} on Azure AD".format(mail=resp.json()["mail"])