# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate

# Initialize the database
db = SQLAlchemy()

# For handling database migrations, Flask-Migrate is a useful extension that integrates with Flask and SQLAlchemy. 
migrate = Migrate(app, db)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Specify the view function that handles logins
login_manager.login_message_category = 'info'

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

    return app
