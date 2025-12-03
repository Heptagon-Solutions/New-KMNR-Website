from flask import Blueprint, request
import base64
from database import db, DatabaseError

shows_bp = Blueprint("shows", __name__)


def _get_current_semester_id(cur):
    cur.execute(
        """
        SELECT id
        FROM semester
        ORDER BY year DESC,
                 FIELD(semester, 'Fall', 'Summer', 'Spring') DESC
        LIMIT 1
        """
    )
    row = cur.fetchone()
    return row["id"] if row else None


@shows_bp.post("/shows")
def create_show():
    data = request.get_json(force=True, silent=True) or {}

    name = data.get("name")
    short_desc = data.get("short_desc")
    long_desc = data.get("long_desc")
    day = data.get("day")               # e.g. 'Monday'
    start_time = data.get("start_time") # 0-23
    end_time = data.get("end_time")     # 0-23
    semester_id = data.get("semester_id")
    show_image = data.get("show_image")

    if not name:
        return {"message": "name is required"}, 400

    try:
        with db.connection.cursor() as cur:
            # if no semester given use current
            if semester_id is None:
                semester_id = _get_current_semester_id(cur)
                if semester_id is None:
                    return {"message": "no semesters exist yet"}, 400
            else:
                # verify semester exists
                cur.execute("SELECT id FROM semester WHERE id = %s", (semester_id,))
                if cur.fetchone() is None:
                    return {"message": "semester_id does not exist"}, 400

            # defaults for time slot if not provided
            if day is None:
                day = "Sunday"
            if start_time is None:
                start_time = 0
            if end_time is None:
                end_time = 1

            cur.execute(
                """
                INSERT INTO radio_show
                    (name, short_desc, long_desc, day, start_time, end_time, semester_id, show_image)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    name,
                    short_desc,
                    long_desc,
                    day,
                    int(start_time),
                    int(end_time),
                    semester_id,
                    show_image,
                ),
            )
            show_id = cur.lastrowid

        db.connection.commit()
        return {
            "id": show_id,
            "name": name,
            "short_desc": short_desc,
            "long_desc": long_desc,
            "day": day,
            "start_time": start_time,
            "end_time": end_time,
            "semester_id": semester_id,
        }, 201
    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@shows_bp.get("/shows")
def list_shows():
    try:
        with db.connection.cursor() as cur:
            semester_id = request.args.get("semester_id", type=int)
            if semester_id is None:
                semester_id = _get_current_semester_id(cur)
                if semester_id is None:
                    return {"message": "no semesters exist yet"}, 400

            # Get shows
            cur.execute(
                """
                SELECT rs.id, rs.name, rs.short_desc, rs.long_desc, rs.day,
                       rs.start_time, rs.end_time, rs.semester_id, rs.show_image
                FROM radio_show rs
                WHERE rs.semester_id = %s
                ORDER BY FIELD(rs.day, 'Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'),
                         rs.start_time
                """,
                (semester_id,),
            )
            shows = list(cur.fetchall())

            # Attach hosts for each show
            for s in shows:
                img_bytes = s.get("show_image")
                if img_bytes is not None:
                    s["show_image"] = base64.b64encode(img_bytes).decode("utf-8")

                cur.execute(
                    """
                    SELECT sh.dj_id, dj.dj_name, u.name as user_name, u.email as user_email
                    FROM show_host sh
                    JOIN dj ON dj.id = sh.dj_id
                    LEFT JOIN `user` u ON u.id = dj.id
                    WHERE sh.radio_show_id = %s
                    """,
                    (s["id"],),
                )
                hosts = list(cur.fetchall())
                s["hosts"] = hosts

        return shows
    except DatabaseError as e:
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@shows_bp.get("/shows/<int:show_id>")
def get_show(show_id: int):
    try:
        with db.connection.cursor() as cur:
            cur.execute(
                "SELECT * FROM radio_show WHERE id = %s",
                (show_id,),
            )
            show = cur.fetchone()
            if show is None:
                return {"message": "show not found"}, 404

            img_bytes = show.get("show_image")
            if img_bytes is not None:
                show["show_image"] = base64.b64encode(img_bytes).decode("utf-8")

            cur.execute(
                """
                SELECT sh.dj_id, dj.dj_name, u.name as user_name, u.email as user_email
                FROM show_host sh
                JOIN dj ON dj.id = sh.dj_id
                LEFT JOIN `user` u ON u.id = dj.id
                WHERE sh.radio_show_id = %s
                """, 
                (show_id,),
            )
            show["hosts"] = list(cur.fetchall())

        return show
    except DatabaseError as e:
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@shows_bp.patch("/shows/<int:show_id>")
def update_show(show_id: int):
    data = request.get_json(force=True, silent=True) or {}

    allowed = {
        "name": "name = %s",
        "short_desc": "short_desc = %s",
        "long_desc": "long_desc = %s",
        "day": "day = %s",
        "start_time": "start_time = %s",
        "end_time": "end_time = %s",
        "semester_id": "semester_id = %s",
        "show_image": "show_image = %s",
    }

    fields = []
    values = []

    if "semester_id" in data:
        try:
            with db.connection.cursor() as cur:
                cur.execute("SELECT id FROM semester WHERE id = %s", (data["semester_id"],))
                if cur.fetchone() is None:
                    return {"message": "semester_id does not exist"}, 400
        except DatabaseError as e:
            return {"message": f"{e.args[1]} ({e.args[0]})"}, 500

    for key, clause in allowed.items():
        if key in data:
            fields.append(clause)
            values.append(data[key])

    if not fields:
        return {"message": "no updatable fields provided"}, 400

    values.append(show_id)
    try:
        with db.connection.cursor() as cur:
            cur.execute(
                f"UPDATE radio_show SET {', '.join(fields)} WHERE id = %s",
                tuple(values),
            )
            updated = cur.rowcount

            if updated == 0:
                cur.execute("SELECT id FROM radio_show WHERE id = %s", (show_id,))
                exists = cur.fetchone() is not None
                if not exists:
                    db.connection.rollback()
                    return {"message": "show not found"}, 404
                db.connection.commit()
                return {"message": "show updated"}, 200

        db.connection.commit()
        return {"message": "show updated"}, 200
    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@shows_bp.post("/shows/<int:show_id>/hosts")
def add_hosts(show_id: int):
    data = request.get_json(force=True, silent=True) or {}
    dj_ids = []

    if "dj_id" in data:
        dj_ids = [int(data["dj_id"])]
    elif "dj_ids" in data:
        dj_ids = [int(x) for x in data["dj_ids"]]
    else:
        return {"message": "dj_id or dj_ids required"}, 400

    try:
        with db.connection.cursor() as cur:
            cur.execute("SELECT id FROM radio_show WHERE id = %s", (show_id,))
            if cur.fetchone() is None:
                return {"message": "show not found"}, 404

            added = []
            for dj_id in dj_ids:
                cur.execute("SELECT id FROM dj WHERE id = %s", (dj_id,))
                if cur.fetchone() is None:
                    # skip invalid dj_id
                    continue

                cur.execute(
                    "SELECT 1 FROM show_host WHERE radio_show_id = %s AND dj_id = %s",
                    (show_id, dj_id),
                )
                if cur.fetchone() is None:
                    cur.execute(
                        "INSERT INTO show_host (radio_show_id, dj_id) VALUES (%s, %s)",
                        (show_id, dj_id),
                    )
                    added.append(dj_id)

        db.connection.commit()
        return {"added": added}, 201
    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@shows_bp.delete("/shows/<int:show_id>/hosts/<int:dj_id>")
def remove_host(show_id: int, dj_id: int):
    try:
        with db.connection.cursor() as cur:
            cur.execute(
                "DELETE FROM show_host WHERE radio_show_id = %s AND dj_id = %s",
                (show_id, dj_id),
            )
            if cur.rowcount == 0:
                db.connection.rollback()
                return {"message": "host not found"}, 404
        db.connection.commit()
        return "", 204
    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@shows_bp.delete("/shows/<int:show_id>")
def delete_show(show_id: int):
    try:
        with db.connection.cursor() as cur:
            cur.execute("DELETE FROM show_host WHERE radio_show_id = %s", (show_id,))
            cur.execute("DELETE FROM rented_show WHERE radio_show_id = %s", (show_id,))
            cur.execute("DELETE FROM radio_show WHERE id = %s", (show_id,))
            if cur.rowcount == 0:
                db.connection.rollback()
                return {"message": "show not found"}, 404
        db.connection.commit()
        return "", 204
    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@shows_bp.post("/shows/<int:show_id>/image")
def upload_show_image(show_id: int):
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

        # Store image in DB
        with db.connection.cursor() as cur:
            cur.execute(
                "SELECT id FROM radio_show WHERE id = %s",
                (show_id,)
            )
            if cur.fetchone() is None:
                return {"message": "show not found"}, 404

            cur.execute(
                "UPDATE radio_show SET show_image = %s WHERE id = %s",
                (image_bytes, show_id)
            )

        db.connection.commit()
        return {"message": "image updated successfully"}, 200

    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f'{e.args[1]} ({e.args[0]})'}, 500