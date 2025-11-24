from flask import Blueprint, request

from database import db, DatabaseError


town_and_campus_news_blueprint = Blueprint("town_and_campus_news", __name__)


DEFAULT_PAGE_SIZE = 200
"""Default number of rows to fetch and return."""


@town_and_campus_news_blueprint.get("/count/news")
def dj_count():
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
