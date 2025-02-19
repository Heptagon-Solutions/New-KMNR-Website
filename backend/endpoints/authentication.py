import datetime, secrets

from flask import current_app, request

from database import db, DatabaseError


EXPIRATION_PERIOD = datetime.timedelta(days=1)


@current_app.post("/login")
def login():
    data = request.json
    print("login post made", data)

    try:
        email = data["email"]
        password = data["pass"]
    except KeyError:
        return {"message": f"Login request must provide 'email' and 'pass'."}, 400

    try:
        with db.connection.cursor() as cur:
            cur.execute(
                f"""SELECT id, email, password, role FROM user WHERE email = '{email}'"""
            )
            user = cur.fetchone()
    except DatabaseError as e:
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500

    if user:
        user_id = user["id"]
        token = create_auth_token(user_id)
        return {
            "message": f"a login request was made for {email} (id={user_id} giving auth token {token})"
        }
    else:
        return {"message": f"No user with email {email} found"}, 404


def create_auth_token(user_id):
    """Generate a auth token for the given user, add it to the database, and return (token, expiration time)."""

    while True:
        token_bytes = secrets.token_bytes(8)
        token = int.from_bytes(token_bytes)

        with db.connection.cursor() as cur:
            cur.execute(
                f"""SELECT id FROM auth_token
                    WHERE token = {token}"""
            )
            if cur.fetchone() is None:
                break

    expiration = datetime.datetime.now() + EXPIRATION_PERIOD
    expiration_string = expiration.isoformat(" ", "seconds")
    try:
        with db.connection.cursor() as cur:
            cur.execute(
                f"""INSERT INTO auth_token (user_id, token, expiration)
                VALUES ({user_id}, {token}, '{expiration_string}')"""
            )
            db.connection.commit()
        return token
    except DatabaseError as e:
        # TODO: Idk what to do here...
        print("AN ERROR OCCURRED", e)
        pass
