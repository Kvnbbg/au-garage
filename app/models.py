from datetime import timedelta

from flask import current_app, session
from flask_login import UserMixin, login_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import get_db_connection, login_manager


class ActivityLog:
    def __init__(self, activity_id, user_id, activity_data):
        self.activity_id = activity_id
        self.user_id = user_id
        self.activity_data = activity_data

    @staticmethod
    def log_activity(user_id, activity_data):
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO activity_log (user_id, activity_data) VALUES (?, ?)",
            (user_id, activity_data),
        )
        conn.commit()
        conn.close()


class Role:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def create_role(name):
        conn = get_db_connection()
        conn.execute("INSERT INTO roles (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()

    @staticmethod
    def find_by_name(name):
        conn = get_db_connection()
        role_row = conn.execute(
            "SELECT * FROM roles WHERE name = ?", (name,)
        ).fetchone()
        conn.close()
        if role_row:
            return Role(name=role_row["name"])
        return None


class User(UserMixin):
    def __init__(
        self,
        id=None,
        username=None,
        email=None,
        password=None,
        role_id=None,
        password_hash=None,
    ):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = (
            password_hash
            if password_hash
            else (generate_password_hash(password) if password else None)
        )
        self.role_id = role_id

    @staticmethod
    def find_by_username(username):
        conn = get_db_connection()
        user_row = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()
        if user_row:
            return User(
                id=user_row["id"],
                username=user_row["username"],
                email=user_row["email"],
                password_hash=user_row["password_hash"],
                role_id=user_row["role_id"],
            )
        return None

    @staticmethod
    def find_by_id(user_id):
        conn = get_db_connection()
        user_row = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        if user_row:
            return User(
                id=user_row['id'],
                username=user_row['username'],
                email=user_row['email'],
                password_hash=user_row['password_hash'],
                role_id=user_row.get('role_id')  # Use .get in case 'role_id' is not in the result
                )
        return None

    def save_to_db(self):
        conn = get_db_connection()
        if self.id is None:
            # Insert new user
            conn.execute(
                "INSERT INTO users (username, email, password_hash, role_id) VALUES (?, ?, ?, ?)",
                (self.username, self.email, self.password_hash, self.role_id),
            )
        else:
            # Update existing user
            conn.execute(
                "UPDATE users SET username = ?, email = ?, password_hash = ?, role_id = ? WHERE id = ?",
                (self.username, self.email, self.password_hash, self.role_id, self.id),
            )
        conn.commit()
        conn.close()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """Return the id of the user to satisfy Flask-Login's requirements."""
        return str(self.id)

    def __repr__(self):
        return f"<User {self.username}>"

class DBHandler:
    @staticmethod
    def add(user):
        with get_db_connection() as conn:
            if isinstance(user, User):
                conn.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                    (user.username, user.email, user.password_hash),
                )

    @staticmethod
    def commit():
        with get_db_connection() as conn:
            conn.commit()  # Commit the changes to the database


class QueryHandler:
    def filter_by(self, **kwargs):
        # Simplified example for username lookup
        if "username" in kwargs:
            with get_db_connection() as conn:
                user_row = conn.execute(
                    "SELECT * FROM users WHERE username = ?", (kwargs["username"],)
                ).fetchone()
                if user_row:
                    return User(
                        username=user_row["username"],
                        email=user_row["email"],
                        password=user_row["password_hash"],
                    )
        return None


# Mimicking 'db' from SQLAlchemy
db = DBHandler()


@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user_row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if user_row:
        return User(
            id=user_row["id"], username=user_row["username"]
        )  # Adjust according to your User class definition
    return None


def login_user_with_expiration(user, remember=True, duration=365):
    login_user(user, remember=remember)
    session.permanent = True
    current_app.permanent_session_lifetime = timedelta(days=duration)


def init_roles():
    roles = ["admin", "editor", "viewer"]
    for role_name in roles:
        if Role.find_by_name(role_name) is None:
            Role.create_role(role_name)
