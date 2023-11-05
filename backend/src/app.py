from configparser import ConfigParser
from dotenv import dotenv_values

from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    config = ConfigParser()
    config.read("../config.ini")
    db_config = config["DATABASE"]
    secrets = dotenv_values("../.env")

    app.config["MYSQL_HOST"] = db_config["host"]
    app.config["MYSQL_PORT"] = int(db_config["port"])
    app.config["MYSQL_DB"] = db_config["database"]
    app.config["MYSQL_USER"] = secrets["DB_USER"]
    app.config["MYSQL_PASSWORD"] = secrets["DB_PASS"]
    app.config[
        "MYSQL_CURSORCLASS"
    ] = "DictCursor"  # Makes cursor.execute() return Dict or Dict[]

    from database import db

    db.init_app(app)

    # THIS IS FOR DEV ONLY - REMOVE BEFORE PRODUCTION
    CORS(app, origins=["http://localhost:4200"])

    with app.app_context():
        import endpoints

        return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
