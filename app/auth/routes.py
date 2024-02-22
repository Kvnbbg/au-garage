# auth/routes.py
from flask import Blueprint, render_template, redirect, url_for

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/logout')
def logout():
    # Logic for logging out users
    return redirect(url_for('main.home'))
