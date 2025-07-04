# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=run:app
ENV FLASK_ENV=development
# Note: For production, FLASK_ENV should be 'production'
# and FLASK_DEBUG should be 0 or not set.
# SECURET_KEY and DATABASE_URL should be passed as env vars at runtime for production.

# Set the working directory in the container
WORKDIR /app

# Install system dependencies that might be needed by Python packages
# Example: RUN apt-get update && apt-get install -y some-package && rm -rf /var/lib/apt/lists/*
# For now, we'll assume most common deps are covered by the base image or Python packages.
# If issues arise with pip install, some system deps might be needed here.

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the application
# For development, Flask's built-in server can be used.
# For production, Gunicorn is recommended.
# The docker-compose.yml will likely override this for different environments or use Gunicorn directly.
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
