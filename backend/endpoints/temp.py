"""This is a placeholder file to show how files in the endpoints folder will be organized. DELETE THIS once other files are made."""

from flask import current_app


@current_app.route("/endpoints/delete_me")
def delete_me():
    return "<p>This is to test that the endpoints folder is working.</p>"
