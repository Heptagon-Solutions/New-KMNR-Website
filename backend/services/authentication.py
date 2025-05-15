"""Helper functions/facades for authentication checks."""

import secrets
from datetime import datetime
from hashlib import scrypt

from ..database import db


EXPIRATION_PERIOD = datetime.timedelta(days=1)

def generate_salt() -> bytes:
    return secrets.token_bytes()  # 32 bytes by default


def hash_password(password: str, salt: bytes) -> bytes:
    """Hash password with salt into a 64 byte string."""
    # Output is 64 bytes by default
    return scrypt(password.encode(), salt=salt, n=16384, r=8, p=1)


def check_password(attempt: str, hashed_pass: bytes, salt: bytes) -> bool:
    """Returns true if password matches."""
    hashed_attempt = hash_password(attempt, salt)
    return hashed_attempt == hashed_pass


def create_auth_token(user_id):
    """Generate a auth token for the given user, add it to the database, and return (token, expiration date). Can raise DatabaseError."""

    # TODO: Set the token with IP Address too
    # TODO: Why not just make the token the table's primary key?

    while True:
        token_bytes = secrets.token_bytes(8)
        token = int.from_bytes(token_bytes)

        # Check if that token number already exists
        with db.connection.cursor() as cur:
            cur.execute(
                f"""SELECT id FROM auth_token
                    WHERE token = {token}"""
            )
            if cur.fetchone() is None:
                break

    expiration = datetime.datetime.now() + EXPIRATION_PERIOD
    expiration_string = expiration.isoformat(" ", "seconds")
    with db.connection.cursor() as cur:
        cur.execute(
            f"""INSERT INTO auth_token (user_id, token, expiration)
            VALUES ({user_id}, {token}, '{expiration_string}')"""
        )
        db.connection.commit()
    
    return (token, expiration)


def check_auth_token(auth_token: str) -> int:
    """Returns the user_id associated with the token if valid, otherwise raises TokenNotFoundException, or TokenExpiredException. Can also raise DatabaseError."""
    if auth_token is None:
        return {"message": "No authentication cookie found"}, 400
    
    # Can raise DatabaseError
    with db.connection.cursor() as cur:
        cur.execute(f"SELECT user_id, expiration FROM auth_token WHERE token = {auth_token}")
        token_info = cur.fetchone()
    
    if token_info is None:
        raise TokenNotFoundException
    
    user_id: int = token_info['user_id']
    expiration: datetime = token_info['expiration']

    # Check expiration
    if expiration < datetime.now():
        raise TokenExpiredException

    return user_id


class TokenNotFoundException(Exception):
    pass


class TokenExpiredException(Exception):
    pass
