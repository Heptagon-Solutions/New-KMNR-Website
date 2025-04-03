import datetime, secrets

from flask import current_app, request, make_response
from flask import Response

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

    if user["id"]:
        return login_success(user["id"])
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

    print("DEBUG: Cookies are:", [c for c in request.cookies.lists()])
    auth_cookie = request.cookies.get("auth")
    if auth_cookie:
        print(f"DEBUG: Auth cookie found during login attempt. Token is {auth_cookie}")

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

    if user["id"]:
        return login_success(user["id"])
    else:
        return {"message": f"No user with email {email} found"}, 404
    

@current_app.get('/authenticate')
def autheticate_using_cookie():
    auth_token = request.cookies.get("auth")

    if auth_token is None:
        return {"message": "No authentication cookie found"}, 400
    
    print(f"DEBUG: Auth cookie found. Token is {auth_token}")
    
    try:
        with db.connection.cursor() as cur:
            cur.execute(f"SELECT user_id, expiration FROM auth_token WHERE token = {auth_token}")
            token_info = cur.fetchone()
    except DatabaseError as e:
        m = f"{e.args[1]} ({e.args[0]})"
        print("Database error:", m)
        return {"message": m}, 500
    
    user_id: str = token_info['user_id']
    expiration: datetime = token_info['expiration']

    # Check expiration
    if expiration < datetime.datetime.now():
        # Redirect to login screen?
        return {"message": "Authentication token expired"}, 401

    return {"success": True, "user_id": user_id}


def login_success(user_id) -> Response:
    """Returns response for a successful login and sets user's auth cookie."""

    resp = make_response({"message": f"a login request was made for user_id={user_id}"})
    try:
        set_auth_cookie(resp, user_id)
        # DEV: THIS IS FOR DEV ONLY (and idk if they actually work lol), DELETE FOR PRODUCTION:
        # resp.headers["Access-Control-Allow-Credentials"] = "true"
        # resp.access_control_allow_credentials = True
    except DatabaseError as e:
        # Only occurs if unable to connect to database
        print("Non-critical database error:", e)

    return resp


def set_auth_cookie(resp: Response, user_id):
    """Set a new auth cookie in response for user. Can raise DatabaseError if there is no connection."""

    token, expiration = create_auth_token(user_id)
    print(f"DEBUG: Auth token created for user #{user_id}: {token}")

    resp.set_cookie(
        "auth",
        str(token),
        EXPIRATION_PERIOD,
        expiration,
        # secure=True,  # Only set the cookie over HTTPS; SKIP FOR DEV, ENFORCE FOR PROD
        httponly=True,
        samesite="Lax",
    )


def create_auth_token(user_id):
    """Generate a auth token for the given user, add it to the database, and return (token, expiration time). Can raise DatabaseError if there is no connection."""

    # TODO: Set the token with IP Address too
    # TODO: Why not just make the token the table's primary key?

    while True:
        token_bytes = secrets.token_bytes(8)
        token = int.from_bytes(token_bytes)

        # Check if that token number already exists
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
        return (token, expiration)
    except DatabaseError as e:
        # TODO: Idk what to do here...
        print("AN ERROR OCCURRED", e)
        pass
