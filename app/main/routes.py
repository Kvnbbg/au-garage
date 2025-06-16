from datetime import datetime
from flask import Blueprint, flash, make_response, redirect, render_template, request, url_for, session, current_app
import math
from app import db # Import db
from app.models import VisitCount # Import VisitCount model

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

    # Retrieve maintenance start date from config
    maintenance_start_date_str = current_app.config.get('MAINTENANCE_START_DATE')
    default_maintenance_start_date = datetime(2024, 1, 1, 0, 0, 0)

    if maintenance_start_date_str:
        try:
            maintenance_start_date = datetime.strptime(maintenance_start_date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            flash(f"Invalid MAINTENANCE_START_DATE format. Using default: {default_maintenance_start_date.strftime('%Y-%m-%d %H:%M:%S')}", "danger")
            maintenance_start_date = default_maintenance_start_date
    else:
        flash(f"MAINTENANCE_START_DATE not configured. Using default: {default_maintenance_start_date.strftime('%Y-%m-%d %H:%M:%S')}", "warning")
        maintenance_start_date = default_maintenance_start_date

    formatted_maintenance_start_date = maintenance_start_date.strftime("%Y-%m-%d %H:%M:%S")

    # Calculate the duration since maintenance started in days
    duration_since_maintenance = now - maintenance_start_date
    days_since_maintenance = duration_since_maintenance.days

    # Get the user identifier (session, IP address, or any unique identifier)
    user_id_str = get_user_id()

    # Query or create VisitCount record for the current user
    user_visit_record = VisitCount.query.filter_by(user_id_str=user_id_str).first()
    if user_visit_record:
        user_visit_record.visits += 1
    else:
        user_visit_record = VisitCount(user_id_str=user_id_str, visits=1)
        db.session.add(user_visit_record)
    db.session.commit()

    current_user_visits = user_visit_record.visits

    # Find the user with the maximum visits for the leaderboard
    top_visitor_record = VisitCount.query.order_by(VisitCount.visits.desc()).first()

    max_visits = 0
    max_visits_user_id_str = "N/A"
    if top_visitor_record:
        max_visits = top_visitor_record.visits
        max_visits_user_id_str = top_visitor_record.user_id_str


    # Dynamic messages based on user visit count
    dynamic_messages = [
        f"Site has been in maintenance since {formatted_maintenance_start_date}.",
        f"{days_since_maintenance} days since maintenance began. We apologize for any inconvenience.",
        f"You're on visit {current_user_visits}. We appreciate your dedication during this maintenance period!"
    ]

    # Leaderboard message with a percentage of the user's visits relative to the top visitor
    if current_user_visits >= max_visits and max_visits > 0: # also check max_visits > 0
        leaderboard_message = f"🏆 You're the top visitor with {current_user_visits} visits!"
    elif max_visits > 0: # Check max_visits > 0 before calculating percentage
        percentage_of_top = calculate_percentage(current_user_visits, max_visits)
        leaderboard_message = (
            f"You're ranked below the top visitor ({max_visits_user_id_str}), who has {max_visits} visits. "
            f"You've completed {math.floor(percentage_of_top)}% of the top user's visits. Keep it up!"
        )
    else: # Handle case where VisitCount table is empty or only has current user
        leaderboard_message = "Welcome! Be the first to set a high score on our visit leaderboard!"


    # Select a dynamic message based on the visit count
    message_index = current_user_visits % len(dynamic_messages)
    dynamic_message = dynamic_messages[message_index]

    # Prepare the response and set cookies for tracking user
    response = make_response(render_template(
        "home.html",
        formatted_maintenance_start_date=formatted_maintenance_start_date,
        days_since_maintenance=days_since_maintenance,
        current_user_visits=current_user_visits,
        dynamic_message=dynamic_message,
        leaderboard_message=leaderboard_message
    ))

    secure_cookie = not current_app.config.get('DEBUG', False) and not current_app.config.get('TESTING', False)

    response.set_cookie("last_visited", formatted_now, max_age=60*60*24*365*2, httponly=True, samesite='Lax', secure=secure_cookie)
    # visit_count cookie is no longer the source of truth, but can be kept for other client-side uses or removed.
    # For this exercise, we'll update it to reflect the database value.
    response.set_cookie("visit_count", str(current_user_visits), max_age=60*60*24*365*2, httponly=True, samesite='Lax', secure=secure_cookie)
    response.set_cookie('user_id', user_id_str, max_age=60*60*24*365*2, httponly=True, samesite='Lax', secure=secure_cookie)

    return response

@main.route("/")
@main.route("/home")
def home():
    """
    Renders the home page and displays maintenance and leaderboard messages.
    """
    return improved_home_with_maintenance_date()
@main.route('/vr')
def vr():
    # Your logic here
    return render_template('vr.html')

# Helper decorator for role checking
from functools import wraps
from flask_login import current_user
from flask import flash, redirect, url_for, request # Added request

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login', next=request.url))
            if not current_user.role or current_user.role.name not in allowed_roles:
                flash(f"You do not have permission to access this page. Required roles: {', '.join(allowed_roles)}.", "danger")
                return redirect(url_for('auth.dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@main.route('/maintenance/logs')
@login_required
@role_required(['Admin', 'Maintenance'])
def maintenance_logs():
    return render_template('maintenance/system_logs.html', title="System Logs")

@main.route('/maintenance/health')
@login_required
@role_required(['Admin', 'Maintenance'])
def maintenance_health():
    return render_template('maintenance/app_health.html', title="Application Health")

@main.route('/maintenance/tasks')
@login_required
@role_required(['Admin', 'Maintenance'])
def maintenance_tasks():
    return render_template('maintenance/maintenance_tasks.html', title="Maintenance Tasks")

# Worker Routes
@main.route('/worker/documents')
@login_required
@role_required(['Admin', 'Maintenance', 'Worker'])
def worker_documents():
    return render_template('worker/documents.html', title="Worker Documents")

@main.route('/worker/schedule')
@login_required
@role_required(['Admin', 'Maintenance', 'Worker'])
def worker_schedule():
    return render_template('worker/schedule.html', title="My Schedule")

@main.route('/worker/tasks')
@login_required
@role_required(['Admin', 'Maintenance', 'Worker'])
def worker_tasks():
    return render_template('worker/tasks.html', title="My Tasks")

@main.route('/worker/salary')
@login_required
@role_required(['Admin', 'Maintenance', 'Worker'])
def worker_salary_info():
    return render_template('worker/salary_info.html', title="My Salary Info")
