# main/routes.py
from flask import Blueprint, render_template, flash
import datetime

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    # Get the current date and time
    now = datetime.datetime.now()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")  # Example: 2024-02-29 23:52

    # Create the maintenance message
    message = f"Maintenance scheduled for {formatted_now}. We apologize for any inconvenience."

    # Flash the message
    flash(message, 'warning')  # 'info' is the category of the message
    flash('🚗💥🎉🕒🔥', 'info')
    return render_template('home.html')
