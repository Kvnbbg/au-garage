# The above class defines different configurations for a Flask application, including a base
# configuration, development configuration, testing configuration, and production configuration.
# config.py
import secrets


class Config:
    SECRET_KEY = secrets.token_hex(32)
    DATABASE_URI = "sqlite:///user.db"


class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = "sqlite:///test.db"

class ProductionConfig(Config):
    DEBUG = False
