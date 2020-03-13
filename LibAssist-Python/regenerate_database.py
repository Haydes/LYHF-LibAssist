#!/usr/bin/env python3
# This script is used to recreate the file library.db with some default values.
# As the database is not committed to github (it's a binary file), and we may
# wish to change the values in it by default, anything to be added to the
# database shohuld be put in this script.


from UserController import create_user
import sqlite3
import os

DB_FILENAME = 'library.db'


# Delete the database and populate it with empty tables.
def regenerate_tables():
    if os.path.exists(DB_FILENAME):
        os.remove(DB_FILENAME)
    conn = sqlite3.connect(DB_FILENAME)
    with open('model.sql', 'r') as model:
        script = model.read()
        conn.executescript(script)
    conn.commit()
    conn.close()


# Repopulate the user table
def regenerate_users():
    create_user('Jack', 'ilovefruits')
    create_user('Jill', 'iloveapples')


if __name__ == '__main__':
    regenerate_tables()
    regenerate_users()
