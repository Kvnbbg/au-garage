import logging
from urllib.parse import urljoin, urlparse

from flask import Blueprint, config, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app.models import User, db, ActivityLog, Role
from werkzeug.security import check_password_hash, generate_password_hash

from app.email import (
    send_email,
)
from flask import current_app

from .forms import (
    EditProfileForm,
    LoginForm,
    RegistrationForm,
    ResetPasswordForm,
    ResetPasswordRequestForm,
    AdminEditUserRoleForm,
)
from app import limiter

auth = Blueprint("auth", __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@auth.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_username(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for("auth.dashboard"))
        flash("Invalid username or password")
    return render_template("login.html", form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        default_role_name = 'Client'
        default_role = Role.find_by_name(default_role_name)
        if not default_role:
            # This case should ideally not happen if init_roles is always run
            logger.error(f"Default role '{default_role_name}' not found. Please initialize roles.")
            flash("An error occurred during registration. Default role not found.", "danger")
            return render_template("register.html", title="Register", form=form)

        new_user = User(username=form.username.data, email=form.email.data, role_id=default_role.id)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        # Log in the new user
        login_user(new_user)
        flash("Your account has been created and you are now logged in.", "success")
        return redirect(url_for("auth.dashboard"))
    return render_template("register.html", title="Register", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))


def is_safe_url(target):
    try:
        test_url = urlparse(urljoin(request.host_url, target))
        # Ensure the URL is either relative or matches the host
        return (
            test_url.scheme in ("http", "https")
            and test_url.netloc == ""
            or test_url.hostname == urlparse(request.host_url).hostname
        )
    except ValueError:
        # If parsing fails, the URL is not safe
        return False




@auth.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    # The form now takes original_username and original_email for validation
    form = EditProfileForm(original_username=current_user.username, original_email=current_user.email)

    is_admin = current_user.role and current_user.role.name == 'Admin'

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data.lower().strip()

        if is_admin and form.role.data is not None:
            admin_role = Role.find_by_name('Admin')
            if current_user.role_id == admin_role.id and form.role.data != admin_role.id:
                admin_count = User.query.filter_by(role_id=admin_role.id).count()
                if admin_count == 1:
                    flash("You are the last admin and cannot change your own role.", "danger")
                    return redirect(url_for('auth.profile'))

            new_role = Role.query.get(form.role.data)
            if new_role:
                current_user.role_id = new_role.id
            else:
                flash("Invalid role selected.", "danger")

        db.session.commit()
        flash("Your profile has been updated.", "success")
        return redirect(url_for("auth.profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        if is_admin and current_user.role_id is not None:
            form.role.data = current_user.role_id
        elif not is_admin: # If not admin, remove the role field from the form to prevent submission
            del form.role

    return render_template("profile.html", title="Edit Profile", form=form, is_admin=is_admin)


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
        sender=current_app.config["ADMINS"][0], # Use current_app.config
        recipients=[user.email],
        text_body=render_template("email/reset_password.txt", user=user, token=token),
        html_body=render_template("email/reset_password.html", user=user, token=token),
    )

@auth.route("/dashboard")
@login_required
def dashboard():
    flash("Welcome to the dashboard! Be careful as you navigate. Try running the different activities through movements in front.", "info")
    return render_template("dashboard.html")

@auth.route("/role")
@login_required
def  role():
    # Example of extending dashboard functionality
    activities = None
    if current_user.role and current_user.role.name == "admin":
        # Fetch admin-specific data or activities
        activities = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).all()
    return render_template("dashboard.html", activities=activities)


# Flask application error handlers
@auth.app_errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@auth.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("500.html"), 500


@auth.route("/admin/users", methods=["GET"])
@login_required
def admin_user_list():
    if not current_user.role or current_user.role.name != 'Admin':
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for('main.home'))

    users = User.query.all()
    return render_template("admin/user_list.html", users=users, title="User List")


@auth.route("/admin/edit_user_role/<int:user_id>", methods=["GET", "POST"])
@login_required
def admin_edit_user_role(user_id):
    if not current_user.role or current_user.role.name != 'Admin':
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for('main.home'))

    user_to_edit = User.query.get_or_404(user_id)
    form = AdminEditUserRoleForm(obj=user_to_edit) # Pre-populate form with user's current role

    if form.validate_on_submit():
        new_role_id = form.role.data
        # Prevent admin from changing their own role via this form to avoid self-lockout
        # or demoting the last admin. More complex logic might be needed for "last admin" scenarios.
        if user_to_edit.id == current_user.id and user_to_edit.role_id != new_role_id :
             flash("Admins cannot change their own role through this form.", "warning")
             return redirect(url_for('auth.admin_user_list'))

        user_to_edit.role_id = new_role_id
        db.session.add(user_to_edit)
        db.session.commit()
        flash(f"Role for user {user_to_edit.username} updated successfully.", "success")
        return redirect(url_for('auth.admin_user_list'))

    if request.method == "GET" and user_to_edit.role:
         form.role.data = user_to_edit.role_id # Ensure correct pre-population on GET

    return render_template("admin/edit_user_role.html", form=form, user_to_edit=user_to_edit, title="Edit User Role")
