from flask import Blueprint, request
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