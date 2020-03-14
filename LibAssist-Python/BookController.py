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


# Get a book associated with some ISBN
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

# show all the books not checked out by others
def show_books():
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT ISBN, title, author, pubDate, username FROM book where username is null"
        )

        tups = cursor.fetchall()
        if tups is None:
            return None
        bookList = list()
        for i in range(len(tups)):
            ISBN = tups[i][0]
            title = tups[i][1]
            author = tups[i][2]
            pubDate = tups[i][3]
            username = tups[i][4]
            book = b.Book(ISBN, title, author, pubDate, username)
            bookList.append(book)

        return bookList

