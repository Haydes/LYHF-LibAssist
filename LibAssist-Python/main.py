#!/usr/bin/env python3

from flask import Flask, redirect, render_template, request, session, url_for
from UserController import validate_user, create_user
from sqlite3 import IntegrityError

app = Flask(__name__)
app.secret_key = b"Totally secret"


# Display landing page for website
@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('mainpage.html', name=username)
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
