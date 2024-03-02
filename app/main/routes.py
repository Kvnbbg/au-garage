# main/routes.py
from flask import Blueprint, render_template, flash
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    flash('🚗💥🎉🕒🔥', 'info')
    return render_template('home.html')
