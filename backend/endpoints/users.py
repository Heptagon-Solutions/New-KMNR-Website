from flask import Blueprint, request
from database import db, DatabaseError

users_bp = Blueprint("accounts", __name__)


@users_bp.post("/users")
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
        try:
            err_code = e.args[0]
        except Exception:
            err_code = None

        if err_code == 1062:
            return {"message": "Could not create account with provided data"}, 409

        return {"message": "Could not create account"}, 500



@users_bp.delete("/users/<int:user_id>")
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


@users_bp.post("/djs")
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

            # check training semester exists
            cur.execute("SELECT id FROM semester WHERE id = %s", (training_semester_id,))
            if cur.fetchone() is None:
                return {"message": "training_semester_id does not exist"}, 400

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
            "profile_desc": profile_desc,
            "profile_img": profile_img,
        }, 201
    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@users_bp.delete("/djs/<int:dj_id>")
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


@users_bp.get("/djs")
def list_djs():
    try:
        with db.connection.cursor() as cur:
            cur.execute(
                """
                SELECT
                    dj.id AS id,
                    u.name AS user_name,
                    dj.dj_name AS dj_name,
                    dj.profile_img AS profile_img
                FROM dj
                JOIN user u ON dj.id = u.id
                ORDER BY dj.dj_name ASC
                """
            )
            rows = cur.fetchall()
        return {"djs": rows}, 200
    except DatabaseError as e:
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@users_bp.get("/djs/<int:dj_id>")
def get_dj(dj_id: int):
    try:
        with db.connection.cursor() as cur:
            cur.execute(
                """
                SELECT
                    dj.id AS id,
                    u.name AS user_name,
                    u.email AS user_email,
                    dj.dj_name,
                    dj.training_semester_id,
                    dj.trainer_dj_id,
                    dj.graduating_semester_id,
                    dj.profile_desc,
                    dj.profile_img
                FROM dj
                JOIN user u ON dj.id = u.id
                WHERE dj.id = %s
                """,
                (dj_id,),
            )
            row = cur.fetchone()

        if row is None:
            return {"message": "dj not found"}, 404

        return row, 200
    except DatabaseError as e:
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@users_bp.patch("/djs/<int:dj_id>")
def update_dj(dj_id: int):
    data = request.get_json(force=True, silent=True) or {}

    fields = []
    values = []

    if "dj_name" in data:
        fields.append("dj_name = %s")
        values.append(data["dj_name"])
    if "profile_desc" in data:
        fields.append("profile_desc = %s")
        values.append(data["profile_desc"])
    if "profile_img" in data:
        fields.append("profile_img = %s")
        values.append(data["profile_img"])
    if "graduating_semester_id" in data:
        # verify semester exists before setting FK
        try:
            with db.connection.cursor() as cur:
                cur.execute(
                    "SELECT id FROM semester WHERE id = %s",
                    (data["graduating_semester_id"],),
                )
                if cur.fetchone() is None:
                    return {"message": "graduating_semester_id does not exist"}, 400
        except DatabaseError as e:
            return {"message": f"{e.args[1]} ({e.args[0]})"}, 500

        fields.append("graduating_semester_id = %s")
        values.append(data["graduating_semester_id"])

    if not fields:
        return {"message": "no updatable fields provided"}, 400

    values.append(dj_id)

    try:
        with db.connection.cursor() as cur:
            cur.execute(
                f"UPDATE dj SET {', '.join(fields)} WHERE id = %s",
                tuple(values),
            )
            if cur.rowcount == 0:
                db.connection.rollback()
                return {"message": "dj not found"}, 404

        db.connection.commit()
        return {"message": "dj updated"}, 200
    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500
