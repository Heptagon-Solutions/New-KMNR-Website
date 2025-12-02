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
