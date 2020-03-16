#!/usr/bin/env python3

from flask import Flask, redirect, render_template, request, session, url_for
from UserController import (
    validate_user, create_user, isLibrarian,
    get_ISBN,
    borrow_book_byISBN, borrow_book_byTitle,
    return_book
)
from BookController import get_book, show_books, create_book
from sqlite3 import IntegrityError
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_bytes(32)


# Display landing page for website
@app.route('/')
def index():
    if 'username' in session:
        return mainpage()
    else:
        return render_template('login.html', message=None)


# Attempt to create a user
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    # TODO: Deny usernames that could be used to inject html
    try:
        create_user(username, password)
        return render_template('login.html', message='Success! User created')
    except IntegrityError:
        return render_template('login.html', message='User alredady exists!')


# Attempt to login the user.
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    success = validate_user(username, password)
    if success:
        session['username'] = username
        return redirect(url_for('index'))
    else:
        return render_template('login.html', message='Invalid credentials')


# Handle returning books
@app.route('/checkin', methods=['POST'])
def checkin():
    if 'username' not in session:
        return render_template('login.html', message='You are not logged in')
    username = session['username']
    return_book(username)
    return redirect(url_for('index'))


# Handle checking out a book
@app.route('/checkout', methods=['POST'])
def checkout():
    if 'username' not in session:
        return render_template('login.html', message='You are not logged in')

    bookid = request.form['bookid']
    idtype = request.form['idtype']

    # Extract search method
    borrow_fn = None
    if idtype == 'use-title':
        borrow_fn = borrow_book_byTitle
    elif idtype == 'use-isbn':
        borrow_fn = borrow_book_byISBN
    else:
        return mainpage(msg="Error: must select title or isbn")

    username = session['username']
    result = borrow_fn(bookid, username)

    # 0: No book found
    if result == 0:
        return mainpage(msg='Cannot check out book: Book not found')
    # 1: Book already being borrowed
    elif result == 1:
        return mainpage(msg='Cannot check out book: Book already borrowed')
    # 2: Book successfully borrowed
    elif result == 2:
        return redirect(url_for('index'))
    # Some other return code
    else:
        return mainpage(msg='Cannot check out book: Unknown error')


# Handle logging out
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


# Display all books in database not currently checked out
@app.route('/showbooks', methods=['GET'])
def showbooks_handler():
    books = show_books()
    return render_template('showbooks.html', booklist=books)


# Librarian control panel/admin page
@app.route('/admin', methods=['GET'])
def admin_handler():
    if 'username' not in session:
        return render_template('login.html', message='You are not logged in')

    username = session['username']
    isadmin = isLibrarian(username)
    if not isadmin:
        return mainpage(msg='Only administrative users may access that page')
    return adminpage()


# Add books from librarian control panel
@app.route('/addbook', methods=['POST'])
def addbook():
    if 'username' not in session:
        return render_template('login.html', message='You are not logged in')

    username = session['username']
    isadmin = isLibrarian(username)
    if not isadmin:
        return mainpage(msg='Only administrative users may access that page')

    title = request.form['title']
    isbn = request.form['isbn']
    author = request.form['author']
    pubdate = request.form['pubdate']

    try:
        isbn = int(isbn)
    except ValueError:
        return adminpage(msg='Invalid ISBN (should be integer)')

    create_book(isbn, title, author, pubdate)
    return adminpage(msg='Success! Book entered into database')


# Handle main page with possible message
def mainpage(msg=None):
    template = 'mainpage.html'
    username = session['username']
    isadmin = isLibrarian(username)

    if msg:
        return render_template(
            template, name=username, admin=isadmin,
            book=None, message=msg
        )

    isbn = get_ISBN(username)
    book = None
    if isbn != 0:
        book = get_book(isbn)

    return render_template(
        template, name=username, admin=isadmin,
        book=book, message=msg
    )


# Handle admin page with possible message
def adminpage(msg=None):
    username = session['username']
    return render_template('admin.html', name=username, message=msg)


if __name__ == '__main__':
    app.run('127.0.0.1', 5000)
