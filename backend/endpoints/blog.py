from datetime import datetime

from flask import Blueprint, request

from database import db, DatabaseError


blog_bp = Blueprint("blog", __name__)

DEFAULT_PAGE_SIZE = 200
"""Default number of rows to fetch and return."""

@blog_bp.post("/blog")
def create_blog_post():
    posting_dj = request.form.get("postingDJ")
    title = request.form.get("title")
    content = request.form.get("content")
    image = request.form.get("image")
    submit_date = datetime.now()
    hidden = request.form.get("hidden", False)

    missing = [name for name, value in {
        "postingDJ": posting_dj,
        "title": title,
        "content": content
    }.items() if value is None]

    if missing:
        if len(missing) == 1:
            msg = f"{missing[0]} is required."
        else:
            msg = f"{', '.join(missing[:-1])} and {missing[-1]} are required."
        return {"message": msg}, 400

    new_post_data = {
        "posting_dj": posting_dj,
        "title": title,
        "content": content,
        "image": image,
        "submit_date": submit_date,
        "hidden": hidden,
    }

    try:
        with db.connection.cursor() as cur:
            cur.execute(
                """
                INSERT INTO blog
                    (posting_dj, title, content, image, submit_date, hidden)
                VALUES
                    (%(posting_dj)s, %(title)s, %(content)s, %(image)s, %(submit_date)s, %(hidden)s)
                """,
                new_post_data,
            )
            blog_id = cur.lastrowid
        db.connection.commit()

        response_data = {
            "id": blog_id,
            "postingDJ": new_post_data["posting_dj"],
            "title": new_post_data["title"],
            "content": new_post_data["content"],
            "image": new_post_data["image"],
            "submitDate": new_post_data["submit_date"],
            "hidden": new_post_data["hidden"],
        }
        return response_data, 201
    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@blog_bp.get("/count/blog")
def blog_count():
    try:
        with db.connection.cursor() as cur:
            cur.execute(
                """
                SELECT COUNT(`id`)
                AS `count`
                FROM `blog`
                """
            )
            count = cur.fetchone()["count"]
        return{"count": count}, 200
    except DatabaseError as e:
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@blog_bp.get("/blog")
def get_all_blogs():
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
                SELECT * FROM blog
                ORDER BY submit_date DESC
                LIMIT %s OFFSET %s
                """,
                (count, offset)
            )

            post_data = cur.fetchall()

        posts = []
        for post in post_data:
            posts.append(
                {
                    "id": post["id"],
                    "postingDJ": post["posting_dj"],
                    "title": post["title"],
                    "content": post["content"],
                    "image": post["image"],
                    "submitDate": post["submit_date"],
                    "editDate": post["edit_date"],
                    "hidden": post["hidden"],
                }
            )
        return {"blog": posts}, 200

    except DatabaseError as e:
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@blog_bp.patch("/admin/blog/<int:blog_id>/hidden")
def hide_blog_post(blog_id: int):
    try:
        with db.connection.cursor() as cur:
            cur.execute(
                """
                SELECT id
                FROM blog
                WHERE id = %s
                """,
                (blog_id,)
            )

            if cur.fetchone() is None:
                return {"message": "blog post not found"}, 404

            cur.execute(
                """
                UPDATE blog
                SET hidden = TRUE
                WHERE id = %s
                """,
                (blog_id,)
            )

        db.connection.commit()
        return {"message": "blog post hidden"}, 200

    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@blog_bp.get("/blog/<int:blog_id>")
def get_blog_post(blog_id: int):
    try:
        with db.connection.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM blog
                WHERE id = %s
                """,
                (blog_id,),
            )
            post = cur.fetchone()

        if post is None:
            return {"message": "blog post not found"}, 404

        formatted = {
            "id": post["id"],
            "postingDJ": post["posting_dj"],
            "title": post["title"],
            "content": post["content"],
            "image": post["image"],
            "submitDate": post["submit_date"],
            "editDate": post["edit_date"],
            "hidden": post["hidden"],
        }

        return formatted, 200

    except DatabaseError as e:
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500


@blog_bp.patch("/admin/blog/<int:blog_id>")
def update_blog(blog_id: int):
    data = request.get_json(force=True, silent=True) or {}

    allowed_fields = {
        "title": "title",
        "content": "content",
        "image": "image",
        "hidden": "hidden"
    }

    fields = []
    values = []

    for field_name, db_column_name in allowed_fields.items():
        if field_name in request.form:
            fields.append(f"{db_column_name} = %s")
            values.append(request.form.get(field_name))

    if not fields:
        return {"message": "no updatable fields provided"}, 400

    fields.append("edit_date = %s")
    values.append(datetime.now())

    values.append(blog_id)

    try:
        with db.connection.cursor() as cur:
            cur.execute(
                """
                SELECT id
                FROM blog
                WHERE id = %s
                """,
                (blog_id,)
            )

            if cur.fetchone() is None:
                return {"message": "blog post not found"}, 404

            cur.execute(
                f"""
                UPDATE blog
                SET {', '.join(fields)}
                WHERE id = %s
                """,
                tuple(values)
            )

        db.connection.commit()
        return {"message": "blog updated"}, 200

    except DatabaseError as e:
        db.connection.rollback()
        return {"message": f"{e.args[1]} ({e.args[0]})"}, 500
