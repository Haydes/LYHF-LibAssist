#!/usr/bin/env python3

from flask import Flask, redirect, render_template, request, session, url_for
from UserController import validate_user, create_user, get_ISBN
from BookController import get_book
from sqlite3 import IntegrityError
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_bytes(32)


# Display landing page for website
@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        isbn = get_ISBN(username)
        book = None
        if isbn != 0:
            book = get_book(isbn)
        return render_template('mainpage.html', name=username, bookObj=book)
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


# Handle logging out
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run('127.0.0.1', 5000)
