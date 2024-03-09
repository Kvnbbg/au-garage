# main/routes.py
import datetime

from flask import Blueprint, flash, make_response, render_template, request

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    """
    Renders the home page and displays a maintenance message.

    Returns:
        response: The response object containing the rendered home page.
    """
    # Get the current date and time
    now = datetime.datetime.now()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")  # Example: 2024-02-29 23:52

    # Get the last visited date from the cookie
    last_visited = request.cookies.get('last_visited')

    # Create the maintenance message
    message = f"Maintenance scheduled for {formatted_now}."
    if last_visited:
        # Loop through a list of dynamic messages
        dynamic_messages = [f" Maintenance scheduled since {last_visited}.", " We apologize for any inconvenience.", " Thank you for your patience."]
        for dynamic_message in dynamic_messages:
            message += f" {dynamic_message}"
    # Flash the message
    flash('🔧 🔧', 'info')
    flash(message, 'warning')  # 'info' or 'warning' is the category of the message
    flash('🛠️ ⚙️', 'info')

    # Set the last visited date in the cookie
    response = make_response(render_template('home.html'))
    response.set_cookie('last_visited', formatted_now)

    return response