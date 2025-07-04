import logging
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp, ValidationError, Email, Optional
# from app.database import get_db_connection  # Ensure correct import for database utility # REMOVED
from app.models import User # IMPORT User model

from wtforms import SelectField # Import SelectField
from app.models import Role # Import Role model

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', coerce=int, validators=[Optional()]) # Added role field
    submit = SubmitField('Update Profile')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
        # Populate role choices - this happens when the form is instantiated
        self.role.choices = [(r.id, r.name) for r in Role.query.order_by('name').all()]

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.find_by_username(username.data)
            if user:
                raise ValidationError('This username is already taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data.lower().strip() != self.original_email:
            user = User.query.filter_by(email=email.data.lower().strip()).first()
            if user:
                raise ValidationError('This email address is already registered. Please choose a different one.')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=4, max=25)],
        render_kw={"placeholder": "Username", "class": "form-control"}
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)],
        render_kw={"placeholder": "Password", "class": "form-control"}
    )
    remember_me = BooleanField("Remember Me")  # Add this line for the "Remember Me" checkbox
    submit = SubmitField(
        "Login",
        render_kw={"class": "btn btn-primary"}
    )

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=25), Regexp(r"^[A-Za-z][A-Za-z0-9_.]*$", 0, "Usernames must have only letters, numbers, dots or underscores")], render_kw={"placeholder": "Username", "class": "form-control"})
    email = EmailField("Email (Optional)", validators=[Optional(), Email(message="Please enter a valid email address.")], render_kw={"placeholder": "Email (Optional)", "class": "form-control"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters long."), Regexp(r"^.*(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[\W_]).*$", 0, "Password must contain a letter, a number, and a special character.")], render_kw={"placeholder": "Password", "class": "form-control"})
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")], render_kw={"placeholder": "Confirm Password", "class": "form-control"})
    submit = SubmitField("Sign Up", render_kw={"class": "btn btn-success"})

    def validate_username(self, username):
        user = User.find_by_username(username.data) # Use SQLAlchemy
        if user:
            logger.warning(f"Attempt to register with taken username: {username.data}")
            raise ValidationError('Username already exists. Please choose a different one.')

    def validate_email(self, email):
        if email.data:  # Only validate if email is provided
            user = User.query.filter_by(email=email.data.lower().strip()).first() # Use SQLAlchemy
            if user:
                logger.warning(f"Attempt to register with taken email: {email.data}")
                raise ValidationError("That email is already in use. Please choose a different one.")


class AdminEditUserRoleForm(FlaskForm):
    role = SelectField('Role', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Update Role')

    def __init__(self, *args, **kwargs):
        super(AdminEditUserRoleForm, self).__init__(*args, **kwargs)
        self.role.choices = [(r.id, r.name) for r in Role.query.order_by('name').all()]
