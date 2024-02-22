# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config
from flask_migrate import Migrate
from app.main import main
from app.auth import auth
from app.models import User
from flask_mail import Mail


# Initialize the database
db = SQLAlchemy()

app = Flask(__name__)

# For handling database migrations, Flask-Migrate is a useful extension that integrates with Flask and SQLAlchemy. 
migrate = Migrate(app, db)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Specify the view function that handles logins
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'noreply@kvnbbg-creations.io'
app.config['MAIL_PASSWORD'] = secrets.token_urlsafe(16)
mail = Mail(app)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    # Import and register blueprints
    from app.main.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from main.auth.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # TODO: initialize other extensions like Flask-Mail