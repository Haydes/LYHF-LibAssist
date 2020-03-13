#!/usr/bin/env python3

import sqlite3
import bcrypt


# Create a new user. By default, no admin privileges are assumed.
# For librarians, set isadmin=1.
def create_user(username, password, isadmin=0):
    pwutf8 = bytes(password, 'utf-8')
    hashed = bcrypt.hashpw(pwutf8, bcrypt.gensalt(12))
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            (username, hashed, isadmin)
        )
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
