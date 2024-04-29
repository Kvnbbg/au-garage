# Garage Web Application

![Preview](https://au-garage-92dd5c42a6c4.herokuapp.com/)

## Overview

Garage V. Parrot, founded by Vincent Parrot in Toulouse, specializes in providing comprehensive automobile services including repairs, maintenance, and sales of pre-owned vehicles. In today’s digital age, establishing a robust online presence is crucial. Hence, we are committed to launching a web platform that mirrors the excellence and dependability of our services.

![Screenshot 1](app/static/images/screen1.jpg)
![Screenshot 2](app/static/images/screen2.jpg)
![Screenshot 3](app/static/images/screen3.jpg)

## Features

- Emojis for Enhanced Readability: 😊 Enabled
- Programming Paradigm: 🧠 Object-Oriented
- Development Language: 🌐 Python
- Project Focus: 📚 Web Development
- Comments: 📖 Descriptive and Insightful
- Code Structure: 🛠️ Modular and Clean
- Error Handling: 🚫 Comprehensive and Robust

## Project Management Tools

- **Trello Board**: Monitor our project's milestones and tasks via our [Trello board](https://trello.com/b/eR2X9dfh).
- **GitHub Repository**: Access our source code and resources on [GitHub](https://github.com/Kvnbbg/au-garage/).
- **Live Application**: Experience Garage V. Parrot's web application [here](https://au-garage-92dd5c42a6c4.herokuapp.com/).

## Installation and Setup

### Prerequisites

Ensure you have the following installed:
- Python 3.8 or newer
- pip (Python's package manager)
- A SQL database system (e.g., PostgreSQL)

### Installation Guide

1. **Clone the Repository**: Download the project onto your local machine.
    ```bash
    git clone https://github.com/Kvnbbg/au-garage/
    cd au-garage
    ```

2. **Virtual Environment Setup**: Create and activate a virtual environment for project dependencies.
    ```bash
    # For Unix/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3. **Install Dependencies**: Install required packages using pip.
    ```bash
    pip install -r requirements.txt
    ```

4. **Database Configuration**: Set up your database connection and initialize the database.
    ```bash
    flask db upgrade
    ```

5. **Set Environment Variables**: Store sensitive information like database URIs in an `.env` file within the project's root directory.

6. **Launch the Application**: Start your Flask server.
    ```bash
    flask run
    ```
    Visit `http://localhost:5000` to access the application.

## Usage

Explore the services offered by Garage V. Parrot via the web application. Users can browse available services, check out pre-owned vehicles, share testimonials, and get in touch with the garage team.

## Contributions

We welcome contributions! For contribution guidelines, please check [CONTRIBUTING.md](https://github.com/Kvnbbg/au-garage/CONTRIBUTING.md).

## License

This project operates under a bespoke license, tailored for both commercial purposes and development flexibility. For more information, refer to [LICENSE.md](https://github.com/Kvnbbg/au-garage/LICENSE.md).

## Contact Us

Should you have any inquiries, suggestions, or wish to contribute, feel free to open an issue in our GitHub repository. Your input is invaluable to us.

Thank you for exploring Garage V. Parrot's web application project.