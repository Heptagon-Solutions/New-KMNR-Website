from io import BytesIO
from flask import Blueprint, request, send_file, url_for
import base64

from database import db, DatabaseError

users_bp = Blueprint("accounts", __name__)


DEFAULT_PAGE_SIZE = 200
"""Default number of rows to fetch and return."""


@users_bp.post("/users")
def create_user():
    data = request.get_json(force=True, silent=True) or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if None in (name, email, password):
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


@users_bp.get("/count/users")
def user_count():
    try:
        with db.connection.cursor() as cur:
            cur.execute("""SELECT COUNT(`id`) AS `count` FROM `user`""")
            count = cur.fetchone()["count"]
        return {"count": count}, 200
    except DatabaseError as e:
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@users_bp.get("/users")
def list_users():
    count = request.args.get("count", default=DEFAULT_PAGE_SIZE, type=int)
    page = request.args.get("page", default=0, type=int)
    offset = page * count

    if count < 1 or page < 0:
        return {
            "message": f"Count must be greater than 0 and Page must be 0 or greater."
        }, 400

    try:
        with db.connection.cursor() as cur:
            cur.execute(
                """
                SELECT
                    `id`,
                    `name`,
                    `email`,
                    `role`
                FROM `user`
                ORDER BY `id` ASC
                LIMIT %s OFFSET %s
                """,
                (count, offset),
            )
            rows = cur.fetchall()
        return {"users": rows}, 200
    except DatabaseError as e:
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@users_bp.get("/users/<int:user_id>")
def get_user(user_id: int):
    try:
        with db.connection.cursor() as cur:
            cur.execute(
                """
                SELECT
                    `id`,
                    `name`,
                    `email`,
                    `role`
                FROM `user`
                WHERE `id` = %s
                """,
                (user_id,),
            )
            row = cur.fetchone()

        if row is None:
            return {"message": "User not found"}, 404

        return row, 200
    except DatabaseError as e:
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@users_bp.post("/djs")
def create_dj():
    data = request.get_json(force=True, silent=True) or {}
    user_id = data.get("userId")
    dj_name = data.get("djName")
    training_semester_id = data.get("trainingSemesterId")

    trainer_dj_id = data.get("trainerId")
    graduating_semester_id = data.get("graduatingSemesterId")
    profile_desc = data.get("profileDesc")
    profile_img = data.get("profileImg")

    if None in (user_id, dj_name, training_semester_id):
        return {"message": "userId, djName, and trainingSemesterId are required"}, 400

    try:
        with db.connection.cursor() as cur:
            cur.execute("SELECT id FROM user WHERE id = %s", (user_id,))
            if cur.fetchone() is None:
                return {"message": "userId does not exist"}, 400

            # check training semester exists
            cur.execute(
                "SELECT id FROM semester WHERE id = %s", (training_semester_id,)
            )
            if cur.fetchone() is None:
                return {"message": "trainingSemesterId does not exist"}, 400

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
            "djName": dj_name,
            "trainingSemesterId": training_semester_id,
            "trainerId": trainer_dj_id,
            "graduatingSemesterId": graduating_semester_id,
            "profileDesc": profile_desc,
            "profileImg": profile_img,
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


@users_bp.get("/count/djs")
def dj_count():
    try:
        with db.connection.cursor() as cur:
            cur.execute("""SELECT COUNT(`id`) AS `count` FROM `dj`""")
            count = cur.fetchone()["count"]
        return {"count": count}, 200
    except DatabaseError as e:
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@users_bp.get("/djs")
def list_djs():
    count = request.args.get("count", default=DEFAULT_PAGE_SIZE, type=int)
    page = request.args.get("page", default=0, type=int)
    offset = page * count

    if count < 1 or page < 0:
        return {
            "message": f"Count must be greater than 0 and Page must be 0 or greater."
        }, 400

    try:
        with db.connection.cursor() as cur:
            cur.execute(
                """
                SELECT
                    `dj`.`id` AS `id`,
                    `u`.`name` AS `userName`,
                    `dj`.`dj_name` AS `djName`,
                    `dj`.`profile_img` IS NOT NULL AS `profileImg`
                FROM `dj`
                JOIN `user` `u` ON `dj`.`id` = `u`.`id`
                ORDER BY `dj`.`id` ASC
                LIMIT %s OFFSET %s
                """,
                (count, offset),
            )
            rows = cur.fetchall()

        for row in rows:
            if row.get("profileImg"):
                row["profileImg"] = url_for(".get_dj_profile_image", dj_id=row["id"])
            else:
                row["profileImg"] = None

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
                    `dj`.`id` AS `id`,
                    `u`.`name` AS `userName`,
                    `u`.`email` AS `userEmail`,
                    `dj`.`dj_name` AS `djName`,
                    `dj`.`training_semester_id` AS `trainingSemesterId`,
                    `dj`.`trainer_dj_id` AS `trainerDJId`,
                    `dj`.`graduating_semester_id` AS `graduatingSemesterId`,
                    `dj`.`profile_desc` AS `profileDesc`,
                    `dj`.`profile_img` IS NOT NULL AS `profileImg`
                FROM `dj`
                JOIN `user` `u` ON `dj`.`id` = `u`.`id`
                WHERE `dj`.`id` = %s
                """,
                (dj_id,),
            )
            row = cur.fetchone()

        if row is None:
            return {"message": "dj not found"}, 404

        if row.get("profileImg"):
            row["profileImg"] = url_for(".get_dj_profile_image", dj_id=dj_id)
        else:
            row["profileImg"] = None

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
            updated = cur.rowcount

            if updated == 0:
                cur.execute("SELECT id FROM dj WHERE id = %s", (dj_id,))
                exists = cur.fetchone() is not None
                if not exists:
                    db.connection.rollback()
                    return {"message": "dj not found"}, 404
                db.connection.commit()
                return {"message": "dj updated"}, 200

        db.connection.commit()
        return {"message": "dj updated"}, 200
    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@users_bp.get("/djs/<int:dj_id>/profile-image")
def get_dj_profile_image(dj_id: int):
    try:
        with db.connection.cursor() as cur:
            cur.execute("SELECT profile_img FROM dj WHERE id = %s", (dj_id,))
            results = cur.fetchone()

        if results is None:
            return {"message": "dj not found"}, 404

        image_bytes: bytes = results.get("profile_img")
        if image_bytes is None:
            return {"message": "dj has no profile image"}, 404

        return send_file(
            BytesIO(image_bytes),
            download_name=f"dj-{dj_id}-profile-image.png",
        )

    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@users_bp.post("/djs/<int:dj_id>/profile-image")
def upload_dj_profile_image(dj_id: int):
    try:
        file = request.files.get("image")

        if file:
            image_bytes = file.read()
        else:
            data = request.get_json(force=True, silent=True) or {}
            image_b64 = data.get("image_base64")

            if not image_b64:
                return {
                    "message": "No image provided. Use multipart 'image' or JSON 'image_base64'."
                }, 400

            try:
                image_bytes = base64.b64decode(image_b64)
            except Exception:
                return {"message": "Invalid base64 image string"}, 400

        with db.connection.cursor() as cur:
            cur.execute("SELECT id FROM dj WHERE id = %s", (dj_id,))
            if cur.fetchone() is None:
                return {"message": "dj not found"}, 404

            cur.execute(
                "UPDATE dj SET profile_img = %s WHERE id = %s",
                (image_bytes, dj_id),
            )

        db.connection.commit()
        return {
            "id": dj_id,
            "profileImg": url_for(".get_dj_profile_image", dj_id=dj_id),
        }, 200

    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500
