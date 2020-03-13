#!/usr/bin/env python3

import sqlite3
import bcrypt


# Create a new book.
def create_book(ISBN, title, author, pubDate):
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO book (ISBN, title, author, pubDate) VALUES (?, ?, ?, ?)",
            (ISBN, title, author, pubDate)
        )
        conn.commit()
