from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# THIS IS FOR DEV ONLY - REMOVE BEFORE PRODUCTION
CORS(app, origins=["http://localhost:4200"])


@app.route("/")
def hello_world():
    return "<p>The backend is working!</p>"


@app.route("/data")
def fake_date():
    return {"msg": "Hi! This is the backend API speaking!"}
