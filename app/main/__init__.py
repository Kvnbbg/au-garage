# main/__init__.py
from flask import Blueprint
import os

# This is the entry point for the application. It creates an instance of the Flask application and runs it.
os.environ["FLASK_ENV"] = "development"
main = Blueprint("main", __name__)
