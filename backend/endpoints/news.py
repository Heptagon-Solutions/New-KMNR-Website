from flask import Blueprint

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
