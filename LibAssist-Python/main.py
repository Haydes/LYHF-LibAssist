#!/usr/bin/env python3

from flask import Flask, redirect, render_template, request, session, url_for
from UserController import (
    validate_user, create_user,
    get_ISBN,
    borrow_book_byISBN, borrow_book_byTitle,
    return_book
)
from BookController import get_book
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


# Handle main page
def mainpage(msg=None):
    template = 'mainpage.html'
    username = session['username']

    if msg:
        return render_template(template, name=username, book=None, message=msg)

    isbn = get_ISBN(username)
    if isbn == 0:
        return render_template(template, name=username, book=None, message=msg)

    book = get_book(isbn)
    return render_template(template, name=username, book=book, message=msg)


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


if __name__ == '__main__':
    app.run('127.0.0.1', 5000)
