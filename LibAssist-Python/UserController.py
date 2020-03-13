#!/usr/bin/env python3

import sqlite3
import bcrypt

_conn = sqlite3.connect("library.db")
_c = _conn.cursor()
_c.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        username text PRIMARY KEY,
        password blob,
        isadmin integer
    )
    """
)
_c.close()
_conn.commit()


# Create a new user with no admin privileges.
def create_user(username, password):
    pwutf8 = bytes(password, 'utf-8')
    hashed = bcrypt.hashpw(pwutf8, bcrypt.gensalt(12))
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users VALUES (?, ?, 0)", (username, hashed))
        conn.commit()


# Determine whether a user exists in the database with a given password.
def validate_user(username, password):
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        tup = cursor.fetchone()

        if tup is None:
            return False

        pwhash = tup[1]
        pwutf8 = bytes(password, 'utf-8')
        return bcrypt.checkpw(pwutf8, pwhash)
