from wtforms.validators import ValidationError
from app.models import User

def validate_username_unique(form, field):
    """
    Validator to check if a username is unique.
    If the form has an `original_username` attribute, it will allow the user to keep their own username.
    """
    original_username = getattr(form, 'original_username', None)
    if field.data != original_username:
        user = User.find_by_username(field.data)
        if user:
            raise ValidationError('This username is already taken. Please choose a different one.')

def validate_email_unique(form, field):
    """
    Validator to check if an email is unique.
    If the form has an `original_email` attribute, it will allow the user to keep their own email.
    """
    original_email = getattr(form, 'original_email', None)
    if field.data.lower().strip() != original_email:
        if field.data: # Only validate if email is provided
            user = User.query.filter_by(email=field.data.lower().strip()).first()
            if user:
                raise ValidationError('That email is already in use. Please choose a different one.')
