from datetime import datetime, timedelta

from flask import current_app, session
from flask_login import UserMixin, login_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login_manager # Import db from app


class ActivityLog(db.Model): # Inherit from db.Model
    __tablename__ = 'activity_log' # Define table name
    activity_id = db.Column(db.Integer, primary_key=True) # Define columns
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    activity_data = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow) # Add timestamp

    @staticmethod
    def log_activity(user_id, activity_data):
        log_entry = ActivityLog(user_id=user_id, activity_data=activity_data)
        db.session.add(log_entry) # Use SQLAlchemy session
        db.session.commit()


class Role(db.Model): # Inherit from db.Model
    __tablename__ = 'roles' # Define table name
    id = db.Column(db.Integer, primary_key=True) # Define columns
    name = db.Column(db.String(80), unique=True, nullable=False)
    color_code = db.Column(db.String(20)) # New column
    hashtag = db.Column(db.String(50))   # New column
    users = db.relationship('User', backref='role', lazy='dynamic') # Define relationship

    def __init__(self, name, color_code=None, hashtag=None):
        self.name = name
        self.color_code = color_code
        self.hashtag = hashtag

    @staticmethod
    def create_role(name, color_code=None, hashtag=None):
        role = Role(name=name, color_code=color_code, hashtag=hashtag)
        db.session.add(role) # Use SQLAlchemy session
        db.session.commit()
        return role # Return the created role

    @staticmethod
    def find_by_name(name):
        return Role.query.filter_by(name=name).first() # Use SQLAlchemy query


class User(UserMixin, db.Model): # Inherit from db.Model
    __tablename__ = 'users' # Define table name
    id = db.Column(db.Integer, primary_key=True) # Define columns
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id')) # Define foreign key
    activity_logs = db.relationship('ActivityLog', backref='user', lazy='dynamic') # Define relationship

    def __init__(self, username=None, email=None, password=None, role_id=None):
        if username:
            self.username = username
        if email:
            self.email = email
        if password:
            self.set_password(password)
        if role_id:
            self.role_id = role_id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first() # Use SQLAlchemy query

    @staticmethod
    def find_by_id(user_id):
        return User.query.get(int(user_id)) # Use SQLAlchemy query

    def save_to_db(self):
        db.session.add(self) # Use SQLAlchemy session
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """Return the id of the user to satisfy Flask-Login's requirements."""
        return str(self.id)

    def __repr__(self):
        return f"<User {self.username}>"

# Remove DBHandler and QueryHandler as SQLAlchemy handles this

# login_manager.user_loader is already updated in app/__init__.py

def login_user_with_expiration(user, remember=True, duration=365):
    login_user(user, remember=remember)
    session.permanent = True
    current_app.permanent_session_lifetime = timedelta(days=duration)


def init_roles():
    # Optional: Clear existing roles for a clean slate if names/IDs might change
    # Warning: This deletes all roles and might affect existing users if not handled carefully.
    # For this exercise, we'll assume it's for initial setup or controlled re-initialization.
    # Role.query.delete()
    # db.session.commit()

    defined_roles = [
        {'name': 'Admin', 'color_code': 'yellow', 'hashtag': '#admin'},
        {'name': 'Maintenance', 'color_code': 'darkgrey', 'hashtag': '#maintenance'},
        {'name': 'Worker', 'color_code': 'blue', 'hashtag': '#worker'},
        {'name': 'Client', 'color_code': 'green', 'hashtag': '#client'}
    ]

    for role_data in defined_roles:
        role = Role.find_by_name(role_data['name'])
        if role is None:
            Role.create_role(name=role_data['name'], color_code=role_data['color_code'], hashtag=role_data['hashtag'])
        else:
            # Optionally update existing roles if attributes changed
            role.color_code = role_data['color_code']
            role.hashtag = role_data['hashtag']
            db.session.add(role)
    db.session.commit()


class VisitCount(db.Model):
    __tablename__ = 'visit_counts'
    id = db.Column(db.Integer, primary_key=True)
    user_id_str = db.Column(db.String(255), unique=True, nullable=False)
    visits = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f"<VisitCount user_id_str={self.user_id_str} visits={self.visits}>"
