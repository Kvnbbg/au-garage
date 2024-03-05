import logging # Import the logging module

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp, ValidationError

from app.models import User

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=25)]
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=4, max=25),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, numbers, dots or underscores",
            ),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, message="Password must be at least 6 characters long."),
            Regexp(
                "^.*(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[\W_]).*$",
                0,
                "Password must contain a letter, a number, and a special character.",
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    # Uncomment the next line to enable Recaptcha
    # recaptcha = RecaptchaField()
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        cleaned_username = username.data.strip()
        user = User.query.filter_by(username=cleaned_username).first()
        if user:
            logger.warning(
                f"Attempt to register with taken username: {cleaned_username}"
            )
            raise ValidationError(
                "That username is taken. Please choose a different one."
            )
