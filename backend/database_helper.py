"""Database helper functions for the new normalized schema with spotipy integration."""

import pymysql
from configparser import ConfigParser
from dotenv import dotenv_values

def get_db_connection():
    """Get a database connection using the configuration."""
    config = ConfigParser()
    config.read("config.ini")
    secrets = dotenv_values(".env")
    
    db_config = config["DATABASE"]
    # Use localhost when testing locally with Docker
    host = 'localhost' if db_config['host'] == 'database' else db_config['host']
    port = 8972 if host == 'localhost' else int(db_config['port'])
    
    connection = pymysql.connect(
        host=host,
        port=port,
        user=secrets["DB_USER"],
        password=secrets["DB_PASS"],
        database=db_config["database"],
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )
    return connection

def get_db_cursor():
    """Get database connection and cursor for the new normalized schema."""
    connection = get_db_connection()
    cursor = connection.cursor()
    return connection, cursor