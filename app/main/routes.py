from datetime import datetime
from flask import Blueprint, flash, make_response, redirect, render_template, request, url_for, session
from collections import Counter
import math

# Global Counter to track visit counts across users (can be replaced by a database in a real-world app)
user_visit_counter = Counter()

main = Blueprint('main', __name__)

@main.route('/set_language/<language>')
def set_language(language):
    session['lang'] = language
    return redirect(url_for('home'))


def calculate_percentage(part, whole):
    """
    Calculate percentage with error handling to avoid division by zero.
    """
    try:
        return (part / whole) * 100
    except ZeroDivisionError:
        return 0


def get_user_id():
    """
    Helper function to retrieve a user identifier, with fallback for missing cookies.
    In real applications, this could be a user session, database lookup, or IP-based tracking.
    """
    user_id = request.cookies.get('user_id')
    if not user_id:
        user_id = 'anonymous_' + str(math.floor(datetime.now().timestamp()))  # Generate unique anonymous ID
    return user_id


def improved_home_with_maintenance_date():
    """
    Renders the home page with dynamic messages and displays the duration since maintenance started.
    Includes user visit count leaderboard, dynamic messages, and handles cookie-related errors.
    """
    # Get the current date and time
    now = datetime.now()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

    # Predefined maintenance start date
    maintenance_start_date = datetime(2024, 1, 1, 0, 0, 0)
    formatted_maintenance_start_date = maintenance_start_date.strftime("%Y-%m-%d %H:%M:%S")

    # Calculate the duration since maintenance started in days
    duration_since_maintenance = now - maintenance_start_date
    days_since_maintenance = duration_since_maintenance.days

    # Get the user identifier (session, IP address, or any unique identifier)
    user_id = get_user_id()

    # Track the user's visit count using cookies, handle cases where cookies are missing
    visit_count = request.cookies.get('visit_count', 0)
    try:
        visit_count = int(visit_count) + 1
    except ValueError:
        visit_count = 1  # Reset visit count if cookie was corrupted

    # Update global visit counter for leaderboard purposes
    user_visit_counter[user_id] += 1

    # Find the user with the maximum visits for the leaderboard
    max_visits_user, max_visits = user_visit_counter.most_common(1)[0]

    # Dynamic messages based on user visit count
    dynamic_messages = [
        f"Site has been in maintenance since {formatted_maintenance_start_date}.",
        f"{days_since_maintenance} days since maintenance began. We apologize for any inconvenience.",
        f"You're on visit {visit_count}. We appreciate your dedication during this maintenance period!"
    ]

    # Leaderboard message with a percentage of the user's visits relative to the top visitor
    if user_visit_counter[user_id] >= max_visits:
        leaderboard_message = f"🏆 You're the top visitor with {user_visit_counter[user_id]} visits!"
    else:
        percentage_of_top = calculate_percentage(user_visit_counter[user_id], max_visits)
        leaderboard_message = (
            f"You're ranked below the top visitor, who has {max_visits} visits. "
            f"You've completed {math.floor(percentage_of_top)}% of the top user's visits. Keep it up!"
        )

    # Select a dynamic message based on the visit count
    message_index = visit_count % len(dynamic_messages)
    dynamic_message = dynamic_messages[message_index]

    # Flash the dynamic message and leaderboard status
    flash(dynamic_message, "warning")  # Maintenance notice
    flash(leaderboard_message, "info")  # Leaderboard notice

    # Prepare the response and set cookies for tracking user
    response = make_response(render_template("home.html"))
    response.set_cookie("last_visited", formatted_now, max_age=60*60*24*365*2, httponly=True, samesite='Lax')  # 2 years, secure cookie
    response.set_cookie("visit_count", str(visit_count), max_age=60*60*24*365*2, httponly=True, samesite='Lax')  # 2 years
    response.set_cookie('user_id', user_id, max_age=60*60*24*365*2, httponly=True, samesite='Lax')  # Store user ID securely

    return response

@main.route("/")
@main.route("/home")
def home():
    """
    Renders the home page and displays maintenance and leaderboard messages.
    """
    return improved_home_with_maintenance_date()
