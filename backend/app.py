from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>The backend is working!</p>"


@app.route("/data")
def fake_date():
    return {"msg": "Hi! This is the backend API speaking!"}
