"""This is the Application Factory and entry point for the Flask application."""

from configparser import ConfigParser
from dotenv import dotenv_values

from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    
    config = ConfigParser()
    config.read("config.ini")
    secrets = dotenv_values(".env")
    
    app.secret_key = secrets.get("FLASK_SECRET_KEY", 'your-secret-key-here')

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

    # THIS IS FOR DEV ONLY - REMOVE BEFORE PRODUCTION
    CORS(app, origins=["http://localhost:8970", "http://localhost:4200", "http://127.0.0.1:4200", "http://127.0.0.1:5001"], 
         supports_credentials=True, 
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    # Add a test endpoint
    @app.route('/test')
    def test():
        return {"status": "Backend is running!", "message": "CORS should be working"}

    # Add all endpoints to the app
    with app.app_context():
        from example_endpoints import example_endpoints_blueprint
        from endpoints.news import town_and_campus_news_blueprint

        app.register_blueprint(example_endpoints_blueprint)
        app.register_blueprint(town_and_campus_news_blueprint)
        
        # Import Spotify endpoints
        try:
            from endpoints.spotify import spotify_bp
            app.register_blueprint(spotify_bp)
            print("✅ Spotify endpoints loaded successfully")
        except Exception as e:
            print(f"❌ Failed to load Spotify endpoints: {e}")
            
        # Import Playlist endpoints
        try:
            from endpoints.playlist import playlist_bp
            app.register_blueprint(playlist_bp)
            print("✅ Playlist endpoints loaded successfully")
        except Exception as e:
            print(f"❌ Failed to load Playlist endpoints: {e}")

        return app


if __name__ == "__main__":
    import os
    app = create_app()
    port = int(os.environ.get('FLASK_RUN_PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
