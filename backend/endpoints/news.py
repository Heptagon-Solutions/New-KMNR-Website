from flask import Blueprint

from database import db, DatabaseError


town_and_campus_news_blueprint = Blueprint("town_and_campus_news", __name__)


@town_and_campus_news_blueprint.route("/admin/news")
def get_all_news():
    """Get all entries in town_and_campus_news in the database."""
    try:
        with db.connection.cursor() as cur:
            cur.execute("SELECT * FROM town_and_campus_news ORDER BY submit_date")
            shows = list(cur.fetchall())
        return shows
    except DatabaseError as e:
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500
