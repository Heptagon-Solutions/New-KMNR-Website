from datetime import date, datetime, timedelta

from flask import Blueprint, request

from database import db, DatabaseError


town_and_campus_news_blueprint = Blueprint("town_and_campus_news", __name__)


DEFAULT_PAGE_SIZE = 200
"""Default number of rows to fetch and return."""


@town_and_campus_news_blueprint.post("/news")
def create_news_entry():
    """title, description, location, contactName, contactEmail are required. expirationDate defaults to 30 days from now if not provided."""
    request_data = request.get_json(force=True, silent=True) or {}
    title = request_data.get("title")
    description = request_data.get("description")
    location = request_data.get("location")
    contact_name = request_data.get("contactName")
    contact_email = request_data.get("contactEmail")

    if not all([title, description, location, contact_name, contact_email]):
        return {
            "message": "Missing one or more required fields: title, description, location, contact_name, contact_email."
        }, 400

    # Expiration Date Validation
    raw_expiration_date = request_data.get("expirationDate")
    if raw_expiration_date:
        try:
            expiration_date = date.fromisoformat(raw_expiration_date)
        except ValueError:
            return {"message": f"Invalid expiration_date: {raw_expiration_date}"}, 400

        if expiration_date <= date.today():
            return {
                "message": "expiration_date must be at least one day in the future"
            }, 400
    else:
        expiration_date = date.today() + timedelta(days=30)

    new_entry_data = {
        "title": title,
        "organization": request_data.get("organization"),
        "description": description,
        "location": location,
        "website": request_data.get("website"),
        "contact_name": contact_name,
        "contact_email": contact_email,
        "approved": False,
        "submit_date": datetime.now(),
        "expiration_date": expiration_date,
    }

    try:
        with db.connection.cursor() as cur:
            cur.execute(
                """
                INSERT INTO `town_and_campus_news` (
                    `title`, `organization`, `description`, `location`, `website`, `contact_name`, `contact_email`, `approved`, `submit_date`, `expiration_date`
                ) VALUES (
                    %(title)s, %(organization)s, %(description)s, %(location)s, %(website)s, %(contact_name)s, %(contact_email)s, %(approved)s, %(submit_date)s, %(expiration_date)s
                )
                """,
                new_entry_data,
            )
            entry_id = cur.lastrowid
        db.connection.commit()

        response_data = {
            "id": entry_id,
            "title": new_entry_data["title"],
            "organization": new_entry_data["organization"],
            "description": new_entry_data["description"],
            "location": new_entry_data["location"],
            "website": new_entry_data["website"],
            "contactName": new_entry_data["contact_name"],
            "contactEmail": new_entry_data["contact_email"],
            "approved": new_entry_data["approved"],
            "submitDate": new_entry_data["submit_date"].isoformat(),
            "expirationDate": new_entry_data["expiration_date"].isoformat(),
        }
        return response_data, 201
    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@town_and_campus_news_blueprint.get("/count/news")
def news_count():
    try:
        with db.connection.cursor() as cur:
            cur.execute("""SELECT COUNT(`id`) AS `count` FROM `town_and_campus_news`""")
            count = cur.fetchone()["count"]
        return {"count": count}, 200
    except DatabaseError as e:
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@town_and_campus_news_blueprint.route("/admin/news")
def get_all_news():
    """Get all entries in town_and_campus_news in the database."""
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
                SELECT * FROM town_and_campus_news
                ORDER BY submit_date
                LIMIT %s OFFSET %s
                """,
                (count, offset),
            )

            entries_data = cur.fetchall()

        entries = []
        for entry in entries_data:
            # Frontend expects responses in lowerCamelCase, not snake_case
            # TODO: Could probably find a better, more reusable way of doing this
            entries.append(
                {
                    "id": entry["id"],
                    "title": entry["title"],
                    "organization": entry["organization"],
                    "description": entry["description"],
                    "location": entry["location"],
                    "website": entry["website"],
                    "contactName": entry["contact_name"],
                    "contactEmail": entry["contact_email"],
                    "approved": entry["approved"],
                    "submitDate": entry["submit_date"],
                    "expirationDate": entry["expiration_date"],
                }
            )
        return {"townAndCampusNews": entries}
    except DatabaseError as e:
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@town_and_campus_news_blueprint.patch("/admin/news/<int:news_id>/approve")
def approve_news(news_id: int):
    """Approve a town_and_campus_news entry by setting approved = TRUE."""
    try:
        with db.connection.cursor() as cur:
            cur.execute(
                "SELECT id FROM town_and_campus_news WHERE id = %s",
                (news_id,)
            )
            if cur.fetchone() is None:
                return {"message": "news entry not found"}, 404

            cur.execute(
                "UPDATE town_and_campus_news SET approved = TRUE WHERE id = %s",
                (news_id,)
            )

        db.connection.commit()
        return {"message": "news approved"}, 200

    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@town_and_campus_news_blueprint.get("/news/<int:news_id>")
def get_news(news_id: int):
    try:
        with db.connection.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM town_and_campus_news
                WHERE id = %s
                """,
                (news_id,),
            )
            entry = cur.fetchone()

        if entry is None:
            return {"message": "news entry not found"}, 404

        formatted = {
            "id": entry["id"],
            "title": entry["title"],
            "organization": entry["organization"],
            "description": entry["description"],
            "location": entry["location"],
            "website": entry["website"],
            "contactName": entry["contact_name"],
            "contactEmail": entry["contact_email"],
            "approved": entry["approved"],
            "submitDate": entry["submit_date"],
            "expirationDate": entry["expiration_date"],
        }

        return formatted, 200

    except DatabaseError as e:
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@town_and_campus_news_blueprint.patch("/admin/news/<int:news_id>")
def update_news(news_id: int):
    data = request.get_json(force=True, silent=True) or {}

    # Mapping of incoming JSON keys → SQL columns
    allowed_fields = {
        "title": "title",
        "organization": "organization",
        "description": "description",
        "location": "location",
        "website": "website",
        "contactName": "contact_name",
        "contactEmail": "contact_email",
        "approved": "approved",
        "expirationDate": "expiration_date",
    }

    fields = []
    values = []

    for json_key, column in allowed_fields.items():
        if json_key in data:
            fields.append(f"{column} = %s")
            values.append(data[json_key])

    if not fields:
        return {"message": "no updatable fields provided"}, 400

    values.append(news_id)

    try:
        with db.connection.cursor() as cur:
            cur.execute(
                "SELECT id FROM town_and_campus_news WHERE id = %s",
                (news_id,)
            )
            if cur.fetchone() is None:
                return {"message": "news entry not found"}, 404

            cur.execute(
                f"UPDATE town_and_campus_news SET {', '.join(fields)} WHERE id = %s",
                tuple(values),
            )

        db.connection.commit()
        return {"message": "news updated"}, 200

    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f'{e.args[1]} ({e.args[0]})'}, 500
