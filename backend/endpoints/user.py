from flask import current_app, request

from database import db, DatabaseError


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
        id = user["id"]
        return {"message": f"a login request was made for {email} (id={id})"}
    else:
        return {"message": f"No user with email {email} found"}, 404
