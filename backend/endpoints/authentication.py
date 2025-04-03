import datetime, secrets

from flask import current_app, request

from database import db, DatabaseError


EXPIRATION_PERIOD = datetime.timedelta(days=1)


@current_app.post("/signup")
def sign_up():
    data = request.json
    print("Attempting to sign up", data)

    try:
        name = data["name"]
        email = data["email"]
        password = data["pass"]
    except KeyError:
        return {
            "message": f"Login request must provide 'name', 'email' and 'pass'."
        }, 400

    try:
        with db.connection.cursor() as cur:
            try:
                cur.execute(
                    f"""INSERT INTO user (name, email, password, role) VALUES ('{name}', '{email}', '{password}', 'dj');"""
                )
            except DatabaseError as e:
                m = f"{e.args[1]} ({e.args[0]})"
                print(f"Database error inserting user {name}:", m)
                return {"message": m}, 500

            try:
                cur.execute("SET sql_auto_is_null = ON;")
                cur.execute("SELECT id FROM user WHERE id IS NULL;")
            except DatabaseError as e:
                m = f"{e.args[1]} ({e.args[0]})"
                print("Database error while selecting added user:", m)
                return {"message": m}, 500

            db.connection.commit()
            user = cur.fetchone()
    except DatabaseError as e:
        m = f"{e.args[1]} ({e.args[0]})"
        print("Database error:", m)
        return {"message": m}, 500

    if user:
        user_id = user["id"]
        set_auth_cookie(user_id)
        return {
            "message": f"Sign-up request for {name} ({email}) successful. Assigned id={user['id']}"
        }
    else:
        return {
            "message": f"We somehow created {email}'s account, but lost their id...?"
        }, 500


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
        m = f"{e.args[1]} ({e.args[0]})"
        print("Database error:", m)
        return {"message": m}, 500

    if user:
        user_id = user["id"]
        set_auth_cookie(user_id)
        return {"message": f"a login request was made for {email} (id={user_id})"}
    else:
        return {"message": f"No user with email {email} found"}, 404


def set_auth_cookie(user_id):
    """Generate a new auth token and set it as a cookie in response."""

    # TODO: STUB function

    token, expiration = create_auth_token(user_id)
    print(f"Auth token created for user #{user_id}: {token}")


def create_auth_token(user_id):
    """Generate a auth token for the given user, add it to the database, and return (token, expiration time)."""

    try:
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
    except DatabaseError as e:
        # TODO: Database connection error
        print("AN ERROR OCCURRED", e)
        pass

    expiration = datetime.datetime.now() + EXPIRATION_PERIOD
    expiration_string = expiration.isoformat(" ", "seconds")
    try:
        with db.connection.cursor() as cur:
            cur.execute(
                f"""INSERT INTO auth_token (user_id, token, expiration)
                VALUES ({user_id}, {token}, '{expiration_string}')"""
            )
            db.connection.commit()
        return (token, expiration)
    except DatabaseError as e:
        # TODO: Idk what to do here...
        print("AN ERROR OCCURRED", e)
        pass
