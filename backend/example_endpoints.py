from flask import current_app

from database import db, DatabaseError


@current_app.route("/")
def hello_world():
    return "<p>The backend is working!</p>"


@current_app.route("/data")
def fake_data():
    return {"msg": "Hi! This is the backend API speaking!"}


# Example endpoint that accesses the database and catches database related errors.
@current_app.route("/database")
def database_test():
    try:
        with db.connection.cursor() as cur:
            cur.execute("""SELECT * FROM radio_show""")
            rv = cur.fetchone()  # Returns a dict
        # Dict and list types are converted to JSON responses
        return rv
    except DatabaseError as e:
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


# Example endpoint that uses URL parameters to make a dynamic database query
# (fyi - this is a TOTALLY unsecure endpoint)
@current_app.route("/database/<table_name>")
def database_table(table_name):
    try:
        with db.connection.cursor() as cur:
            cur.execute(f"""SELECT * FROM {table_name} LIMIT 5""")
            rv = cur.fetchall()  # Returns a tuple
        # Must return list or dict for a JSON response; convert tuples to lists
        return list(rv)
    except DatabaseError as e:
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500
