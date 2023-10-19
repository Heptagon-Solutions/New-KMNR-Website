from configparser import ConfigParser

from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS


app = Flask(__name__)

config = ConfigParser()
config.read("config.ini")
db_config = config["DATABASE"]

app.config["MYSQL_HOST"] = db_config["host"]
app.config["MYSQL_PORT"] = int(db_config["port"])
app.config["MYSQL_DB"] = db_config["database"]
app.config["MYSQL_USER"] = db_config["user"]
app.config["MYSQL_PASSWORD"] = db_config["pass"]
app.config["MYSQL_CURSORCLASS"] = "DictCursor"  # Makes cursor.execute() return Dict or Dict[]
mysql = MySQL(app)

# THIS IS FOR DEV ONLY - REMOVE BEFORE PRODUCTION
CORS(app, origins=["http://localhost:4200"])


@app.route("/")
def hello_world():
    return "<p>The backend is working!</p>"

@app.route("/data")
def fake_data():
    return {"msg": "Hi! This is the backend API speaking!"}

@app.route("/database")
def database_test():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM actor""")
    rv = cur.fetchone()
    cur.close()
    return str(rv)

@app.route("/database/<table_name>")
def database_table(table_name):
    with mysql.connection.cursor() as cur:
        cur.execute(f"""SELECT * FROM {table_name} LIMIT 5""")
        rv = cur.fetchall()
    return str(rv)

if __name__ == "__main__":
    app.run(debug=True)