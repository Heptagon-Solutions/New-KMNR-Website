from flask import Blueprint, request

from database import db, DatabaseError


town_and_campus_news_blueprint = Blueprint("town_and_campus_news", __name__)


@town_and_campus_news_blueprint.route("/admin/news")
def get_all_news():
    """Get all entries in town_and_campus_news in the database."""
    try:
        with db.connection.cursor() as cur:
            cur.execute("SELECT * FROM town_and_campus_news ORDER BY submit_date")

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
        return entries
    except DatabaseError as e:
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@town_and_campus_news_blueprint.post("/news")
def create_news():
    data = request.get_json(force=True, silent=True) or {}

    organization = data.get("organization")
    description = data.get("description")
    location = data.get("location")
    website = data.get("website")
    contact_name = data.get("contactName")
    contact_email = data.get("contactEmail")
    expiration_date = data.get("expirationDate")  # optional

    if not description:
        return {"message": "description is required"}, 400

    try:
        with db.connection.cursor() as cur:
            cur.execute(
                """
                INSERT INTO town_and_campus_news
                    (organization, description, location, website,
                     contact_name, contact_email, approved,
                     submit_date, expiration_date)
                VALUES
                    (%s, %s, %s, %s,
                     %s, %s, %s,
                     NOW(), %s)
                """,
                (
                    organization,
                    description,
                    location,
                    website,
                    contact_name,
                    contact_email,
                    False,
                    expiration_date,
                ),
            )
            new_id = cur.lastrowid

        db.connection.commit()
        return {"id": new_id}, 201
    except DatabaseError as e:
        db.connection.rollback()
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
