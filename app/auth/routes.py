import logging
from urllib.parse import urljoin, urlparse

from flask import Blueprint, config, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app.models import User, db
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import get_db_connection
from app.email import (  # Assuming this function is adapted for direct SQL handling
    send_email,
)

from .forms import (
    EditProfileForm,
    LoginForm,
    RegistrationForm,
    ResetPasswordForm,
    ResetPasswordRequestForm,
)

auth = Blueprint("auth", __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_user_by_username(username):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    return user


def get_user_by_email(email):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return user


def insert_new_user(username, email, password_hash):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (username, email, password_hash),
    )
    conn.commit()
    conn.close()


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)
        if user and check_password_hash(user["password_hash"], form.password.data):
            # User class needs adjustment for Flask-Login without SQLAlchemy
            user_obj = User(
                id=user["id"], username=user["username"]
            )  # Adjust User class as needed
            login_user(user_obj, remember=form.remember_me.data)
            next_page = request.args.get("next")
            if not next_page or not is_safe_url(next_page):
                return redirect(url_for("main.home"))
            return redirect(next_page or url_for("main.home"))
        flash("Invalid username or password")
    return render_template("login.html", form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        insert_new_user(form.username.data, form.email.data, hashed_password)
        flash("Your account has been created, you can now log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", title="Register", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))


def is_safe_url(target):
    test_url = urlparse(urljoin(request.host_url, target))
    return (
        test_url.scheme in ("http", "https")
        and urlparse(request.host_url).hostname == test_url.hostname
    )


@auth.route("/set_language/<language>")
def set_language(language):
    # Check to ensure the language code is supported
    supported_languages = ["en", "fr"]
    if language in supported_languages:
        session["lang"] = language
    else:
        flash("Unsupported language.", "error")
    return redirect(url_for("main.home"))


@auth.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your profile has been updated.", "success")
        return redirect(url_for("auth.profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("profile.html", title="Edit Profile", form=form)


@auth.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Check your email for the instructions to reset your password", "info")
        return redirect(url_for("auth.login"))
    return render_template(
        "reset_password_request.html", title="Reset Password", form=form
    )


@auth.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("main.home"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset.", "success")
        return redirect(url_for("auth.login"))
    return render_template("reset_password.html", form=form)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        "[YourApp] Reset Your Password",
        sender=config["ADMINS"][0],
        recipients=[user.email],
        text_body=render_template("email/reset_password.txt", user=user, token=token),
        html_body=render_template("email/reset_password.html", user=user, token=token),
    )

@auth.route("/dashboard")
@login_required
def dashboard():
    # Example of extending dashboard functionality
    if current_user.role == "admin":
        # Fetch admin-specific data or activities
        conn = get_db_connection()
        activities = conn.execute('SELECT * FROM activity_log').fetchall()
    else:
        activities = None
    return render_template("dashboard.html", activities=activities)


# Flask application error handlers
@auth.app_errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@auth.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("500.html"), 500
