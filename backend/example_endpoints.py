from flask import Blueprint

from database import db, DatabaseError

example_endpoints_blueprint = Blueprint("example_endpoints_plz_delete_later", __name__)


@example_endpoints_blueprint.route("/")
def hello_world():
    return "<p>The backend is working!</p>"


@example_endpoints_blueprint.route("/data")
def fake_data():
    return {"msg": "Hi! This is the backend API speaking!"}


# Example endpoint that accesses the database and catches database related errors.
@example_endpoints_blueprint.route("/database")
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
@example_endpoints_blueprint.route("/database/<table_name>")
def database_table(table_name):
    try:
        with db.connection.cursor() as cur:
            cur.execute(f"""SELECT * FROM {table_name} LIMIT 5""")
            rv = cur.fetchall()  # Returns a tuple
        # Must return list or dict for a JSON response; convert tuples to lists
        return list(rv)
    except DatabaseError as e:
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500
