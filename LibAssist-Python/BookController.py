#!/usr/bin/env python3

import sqlite3
import Book as b


# Create a new book.
def create_book(ISBN, title, author, pubDate):
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO book (ISBN, title, author, pubDate) VALUES (?, ?, ?, ?)",
            (ISBN, title, author, pubDate)
        )
        conn.commit()

def get_book(ISBN):
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT title, author, pubDate, username FROM book where ISBN=?",
            (ISBN,)
        )

    tup = cursor.fetchone()
    if tup is None:
        return None

    title = tup[0]
    author = tup[1]
    pubDate = tup[2]
    username = tup[3]
    book = b.Book(ISBN, title, author, pubDate, username)
    return book
