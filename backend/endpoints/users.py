# endpoints/admin.py
from flask import Blueprint, request
from database import db, DatabaseError

admin_bp = Blueprint("admin", __name__, url_prefix="/api")


@admin_bp.post("/users")
def create_user():
    data = request.get_json(force=True, silent=True) or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not all([name, email, password]):
        return {"message": "name, email, and password are required"}, 400

    try:
        with db.connection.cursor() as cur:
            cur.execute(
                "INSERT INTO user (name, email, password, role) VALUES (%s, %s, %s, %s)",
                (name, email, password, role),
            )
            user_id = cur.lastrowid
        db.connection.commit()
        return {"id": user_id, "name": name, "email": email, "role": role}, 201
    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@admin_bp.delete("/users/<int:user_id>")
def delete_user(user_id: int):
    try:
        with db.connection.cursor() as cur:
            cur.execute("DELETE FROM show_host WHERE dj_id = %s", (user_id,))
            cur.execute("DELETE FROM rented_show WHERE claimer_dj_id = %s", (user_id,))

            cur.execute("DELETE FROM dj WHERE id = %s", (user_id,))

            cur.execute("DELETE FROM user WHERE id = %s", (user_id,))
            if cur.rowcount == 0:
                db.connection.rollback()
                return {"message": "user not found"}, 404

        db.connection.commit()
        return "", 204
    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@admin_bp.post("/djs")
def create_dj():
    data = request.get_json(force=True, silent=True) or {}
    user_id = data.get("user_id")
    dj_name = data.get("dj_name")
    training_semester_id = data.get("training_semester_id")

    trainer_dj_id = data.get("trainer_dj_id")
    graduating_semester_id = data.get("graduating_semester_id")
    profile_desc = data.get("profile_desc")
    profile_img = data.get("profile_img")  

    if not all([user_id, dj_name, training_semester_id]):
        return {"message": "user_id, dj_name, and training_semester_id are required"}, 400

    try:
        with db.connection.cursor() as cur:
            cur.execute("SELECT id FROM user WHERE id = %s", (user_id,))
            if cur.fetchone() is None:
                return {"message": "user_id does not exist"}, 400

            cur.execute(
                """
                INSERT INTO dj
                    (id, dj_name, training_semester_id, trainer_dj_id, graduating_semester_id, profile_desc, profile_img)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    user_id,
                    dj_name,
                    training_semester_id,
                    trainer_dj_id,
                    graduating_semester_id,
                    profile_desc,
                    profile_img,
                ),
            )
        db.connection.commit()
        return {
            "id": user_id,
            "dj_name": dj_name,
            "training_semester_id": training_semester_id,
            "trainer_dj_id": trainer_dj_id,
            "graduating_semester_id": graduating_semester_id,
        }, 201
    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@admin_bp.delete("/djs/<int:dj_id>")
def delete_dj(dj_id: int):
    try:
        with db.connection.cursor() as cur:
            cur.execute("DELETE FROM show_host WHERE dj_id = %s", (dj_id,))
            cur.execute("DELETE FROM rented_show WHERE claimer_dj_id = %s", (dj_id,))

            cur.execute("DELETE FROM dj WHERE id = %s", (dj_id,))
            if cur.rowcount == 0:
                db.connection.rollback()
                return {"message": "dj not found"}, 404

        db.connection.commit()
        return "", 204
    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500
