import datetime, secrets

from flask import current_app, request, make_response
from flask import Response

from ..database import db, DatabaseError
from ..services import authentication as auth_service


@current_app.post("/signup")
def sign_up():
    data = request.json
    print("Attempting to sign up", data)

    try:
        name: str = data["name"]
        email: str = data["email"]
        password: str = data["pass"]
    except KeyError:
        return {
            "message": f"Login request must provide 'name', 'email' and 'pass'."
        }, 400

    try:
        salt = auth_service.generate_salt()
        hashed_pass = auth_service.hash_password(password, salt)

        with db.connection.cursor() as cur:
            try:
                cur.execute(
                    f"""INSERT INTO user (name, email, salt, password_hash, role)
                    VALUES (
                    '{name}',
                    '{email}',
                    UNHEX ('{salt.hex()}'),
                    UNHEX ('{hashed_pass.hex()}'),
                    'dj'
                    );"""
                )
            except DatabaseError as e:
                m = f"{e.args[1]} ({e.args[0]})"
                print(f"Database error inserting user {name}:", m)
                return {"message": m}, 500

            try:
                cur.execute("SET sql_auto_is_null = ON;")
                cur.execute("SELECT id, role FROM user WHERE id IS NULL;")
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
        return login_success(user["id"], user['role'])
    else:
        return {
            "message": f"We somehow created {email}'s account, but lost their id...?"
        }, 500


@current_app.post("/login")
def login():
    data = request.json
    print("login post made", data)

    try:
        email: str = data["email"]
        password_attempt: str = data["pass"]
    except KeyError:
        return {"message": f"Login request must provide 'email' and 'pass'."}, 400

    print("DEBUG: Cookies are:", [c for c in request.cookies.lists()])
    auth_cookie = request.cookies.get("auth")
    if auth_cookie:
        print(f"DEBUG: Auth cookie found during login attempt. Token is {auth_cookie}")

    try:
        with db.connection.cursor() as cur:
            cur.execute(
                f"""SELECT id, email, salt, password_hash, role FROM user WHERE email = '{email}'"""
            )
            user = cur.fetchone()
    except DatabaseError as e:
        m = f"{e.args[1]} ({e.args[0]})"
        print("Database error:", m)
        return {"message": m}, 500

    if user is None:
        # This returns 401 as a security measure. Attackers won't know if it was the password or the email that was bad.
        # TODO: Change this from a debug message to something less obvious of what went wrong.
        return {"message": f"No user with email {email} found"}, 401
    
    if auth_service.check_password(password_attempt, user['password_hash'], user['salt']):
        return login_success(user["id"], user['role'])
    else:
        # TODO: Change this from a debug message to something less obvious of what went wrong.
        # This message should be vague, to ensure attackers don't know if the password was wrong or the email.
        return {"message": "Incorrect password"}, 401
    

@current_app.get('/authenticate')
def authenticate_using_cookie():
    auth_token = request.cookies.get("auth")
    if auth_token is None:
        return {"message": "No authentication cookie found"}, 400
    
    print(f"DEBUG: Auth cookie found. Token is {auth_token}")

    try:
        user_id = auth_service.check_auth_token(auth_token)
    except DatabaseError as e:
        m = f"{e.args[1]} ({e.args[0]})"
        print("Database error:", m)
        return {"message": m}, 500
    except auth_service.TokenNotFoundException:
        return {"message", "The provided authentication token does not exist"}, 401
    except auth_service.TokenExpiredException:
        # Redirect to login screen?
        return {"message": "Authentication token expired"}, 401

    return {
        "success": True,
        "userId": user_id,
        "message": f"User #{user_id} successfully authenticated"
    }


def login_success(user_id: int, user_role: str) -> Response:
    """Returns response for a successful login and sets user's auth cookie."""

    resp = make_response({
        "success": True,
        "userId": user_id,
        "role": user_role
    })
    try:
        set_auth_cookie(resp, user_id)
    except DatabaseError as e:
        # Only occurs if unable to connect to database
        print("Non-critical database error:", e)

    return resp


def set_auth_cookie(resp: Response, user_id):
    """Set a new auth cookie in response for user. Can raise DatabaseError if there is no connection."""

    try:
        token, expiration_date = auth_service.create_auth_token(user_id)
    except DatabaseError as e:
        m = f"{e.args[1]} ({e.args[0]})"
        print("Database error:", m)
        return {"message": m}, 500

    print(f"DEBUG: Auth token created for user #{user_id}: {token}")

    resp.set_cookie(
        "auth",
        str(token),
        auth_service.EXPIRATION_PERIOD,
        expiration_date,
        # Secure means only set the cookie over HTTPS; SKIP FOR DEV, ENFORCE FOR PROD
        # secure=True,
        httponly=True,
        samesite="Lax",
    )
