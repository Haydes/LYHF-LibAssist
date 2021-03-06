#!/usr/bin/env python3

import sqlite3
import bcrypt
from BookController import create_book


# Create a new user. By default, no admin privileges are assumed.
# For librarians, set isadmin=1.
def create_user(username, password, isadmin=0):
    pwutf8 = bytes(password, 'utf-8')
    hashed = bcrypt.hashpw(pwutf8, bcrypt.gensalt(12))
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users(username, password, isadmin) VALUES (?, ?, ?)",
            (username, hashed, isadmin)
        )
        conn.commit()


# Determine whether a user exists in the database with a given password.
def validate_user(username, password):
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password FROM users WHERE username=?",
            (username,)
        )
        tup = cursor.fetchone()

        if tup is None:
            return False

        pwhash = tup[0]
        pwutf8 = bytes(password, 'utf-8')
        return bcrypt.checkpw(pwutf8, pwhash)


def get_ISBN(username):
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT bookISBN FROM users WHERE username=?",
            (username,)
        )

        tup = cursor.fetchone()
        if tup is None:
            return None
        ISBN = tup[0]
        return ISBN


def borrow_book_byISBN(ISBN, username):
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT title, username FROM book where ISBN=?",
            (ISBN,)
        )

        tup = cursor.fetchone()
        if tup is None:
            return 0   # no book found
        user = tup[1]  # username from the book table
        if user is not None:
            return 1   # other user have got the book
        else:
            cursor.execute(
                "UPDATE book SET username=? where ISBN=?",
                (username, ISBN,)
            )
            cursor.execute(
                "UPDATE users SET bookISBN=? where username=?",
                (ISBN, username,)
            )
            conn.commit()
            return 2  # successfully check out


def borrow_book_byTitle(title, username):
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT ISBN, username FROM book where title=?",
            (title,)
        )

        tup = cursor.fetchone()
        if tup is None:
            return 0  # no book found

        ISBN = tup[0]  # isbn from the book table
        user = tup[1]  # username from the book table

        if user is not None:
            return 1  # other user have got the book
        else:
            cursor.execute(
                "UPDATE book SET username=? where ISBN=?",
                (username, ISBN,)
            )
            cursor.execute(
                "UPDATE users SET bookISBN=? where username=?",
                (ISBN, username,)
            )
            conn.commit()
            return 2  # successfully check out


# check whether the user is librarian
def isLibrarian(username):
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT isadmin FROM users WHERE username=?",
            (username,)
        )

        tup = cursor.fetchone()
        if tup is None:
            return False

        isadmin = tup[0]
        if isadmin == 0:
            return False
        else:
            return True


def return_book(username):
    ISBN = get_ISBN(username)
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users set bookISBN=0 WHERE username=?",
            (username,)
        )
        cursor.execute(
            "UPDATE book set username=null WHERE ISBN=?",
            (ISBN,)
        )
        conn.commit()
