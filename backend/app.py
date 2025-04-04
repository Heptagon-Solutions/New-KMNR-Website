""" This is the Application Factory and entry point for the Flask application. """

from configparser import ConfigParser
from dotenv import dotenv_values

from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    config = ConfigParser()
    config.read("config.ini")
    secrets = dotenv_values(".env")

    # Set database configurations
    db_config = config["DATABASE"]
    app.config["MYSQL_HOST"] = db_config["host"]
    app.config["MYSQL_PORT"] = int(db_config["port"])
    app.config["MYSQL_DB"] = db_config["database"]
    app.config["MYSQL_USER"] = secrets["DB_USER"]
    app.config["MYSQL_PASSWORD"] = secrets["DB_PASS"]
    app.config["MYSQL_CURSORCLASS"] = (
        "DictCursor"  # Makes cursor.execute() return Dict or Dict[]
    )

    # Initialize database
    from database import db

    db.init_app(app)

    # TODO: Document that the server machine's public facing IP must be in here
    # TODO: Somehow figure out the frontend's host IP and port and place it here
    CORS(
        app,
        origins=["http://localhost:4200"],
        # TODO: THERE ARE IMPORTANT SECURITY ISSUES ATTACHED TO THIS (CSRF)
        supports_credentials=True
    )

    # Add all endpoints to the app
    with app.app_context():
        import example_endpoints
        import endpoints

        return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
