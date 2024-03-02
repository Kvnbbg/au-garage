# This Python script is the entry point for a Flask application. Here's a breakdown of what it does:
from app import create_app
import os

# This is the entry point for the application. It creates an instance of the Flask application and runs it.
os.environ["FLASK_ENV"] = "development"

app = create_app()

if __name__ == "__main__":
    app.run()
