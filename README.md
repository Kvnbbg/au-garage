# Garage V. Parrot Management System  
**Coding, Gaming & Web Development**  
 
*Design Updates: [Canva Project](https://www.canva.com/design/DAGgJLt8Om8/ZPXG_N-ZqK2XL1trXlw2_g/edit?utm_content=DAGgJLt8Om8&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)*  

---

## Introduction/Overview
Garage V. Parrot is a web application designed to modernize operations for automotive service providers. Originally created for Vincent Parrot of Toulouse, this platform now serves as a scalable solution for garage management. It combines service tracking, customer engagement, and inventory control, all presented through a role-based UI and dashboard system tailored to different user needs (Admin, Maintenance, Worker, Client).

---

## Background  
### Project Origin  
![Logo](https://github.com/Kvnbbg/au-garage/blob/main/app/static/images/logo.png)  
Developed as a capstone project during studies at [STUDI](https://studi.com) (2022–2024), this system was designed to digitize workflows for small automotive businesses. The platform emphasizes reliability, user experience, and adaptability to evolving industry demands.  

### Evolution  
The application has transitioned from a local garage tool to a modular solution for modern entrepreneurs, incorporating advanced features like VR integrations and predictive analytics.  

---

## Key Features  
- **Service Management**: Track repairs, maintenance, and vehicle sales.  
- **Inventory Control**: Real-time stock alerts and automated reordering.  
- **Customer Portal**: Direct communication, appointment booking, and invoice generation.  
- **Role-Based Access Control**: Distinct UIs and permissions for Admin, Maintenance, Worker, and Client roles.
- **Analytics Dashboard**: Performance metrics and reporting tools.
- **Database-backed Visit Tracking**: Monitors user visits with a leaderboard display.
- **Configurable Maintenance Mode**: Allows administrators to display a maintenance notice with a specific start date.
- **Visual Login Indicator**: Provides clear visual feedback on login status.
- **Security Features**: Includes rate limiting to prevent abuse and CSRF protection on forms.

---

## Technical Overview / Architecture
### Core Technologies
- **Backend**: Python, utilizing the Flask framework with an object-oriented design.
- **Database**: PostgreSQL is the target for production, with SQLite often used for development. Interactions are managed via Flask-Migrate and SQLAlchemy ORM.
- **Frontend**: Jinja2 for server-side templating, delivering a responsive UI (assumed to be styled with Bootstrap or a similar framework).
- **Integrations**: SMTP for email notifications, potential for payment gateways, and VR tools.

### Key Libraries & Extensions
- **Flask-Login**: Manages user sessions and authentication.
- **Flask-WTF**: Handles form creation, validation, and CSRF protection.
- **Flask-SQLAlchemy**: Provides ORM capabilities for database interaction.
- **Flask-Migrate**: Manages database schema migrations.
- **Flask-Limiter**: Implements rate limiting for application routes.
- **Flask-Mail**: Facilitates sending emails for notifications and password resets.

### Code Standards  
- Modular, reusable components.  
- Comprehensive error handling and logging.  
- RESTful API structure where applicable.

---

## Setup & Deployment  
### Prerequisites  
- Python 3.8+  
- pip (Python package installer)
- PostgreSQL (for production) or SQLite (for development)

### Installation Steps
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Kvnbbg/au-garage
    cd au-garage
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Unix/macOS
    # For Windows: .\venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up the database:**
    Apply database migrations (creates tables if they don't exist):
    ```bash
    flask db upgrade
    ```
5.  **Initialize roles:**
    Populate the database with predefined user roles:
    ```bash
    flask init-roles
    ```
6.  **Configure environment variables:**
    Create a `.env` file in the root directory and populate it with necessary configurations. See the Configuration section below for details.
7.  **Run the development server:**
    ```bash
    flask run
    ```
    The application should now be accessible at `http://127.0.0.1:5000/`.

### Configuration
Create a `.env` file in the project root with the following variables:
```env
# Core Flask settings
SECRET_KEY='your_very_secret_key_here'  # Replace with a strong random key
FLASK_ENV='development' # or 'production'

# Database settings
DATABASE_URL='postgresql://user:password@host:port/dbname' # For PostgreSQL
# Example for SQLite (development):
# DATABASE_URL='sqlite:///../instance/app.db'

# Email settings (using Flask-Mail)
MAIL_SERVER='smtp.example.com'
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME='your-email@example.com'
MAIL_PASSWORD='your-email-password'
MAIL_DEFAULT_SENDER='noreply@example.com'

# Application-specific settings
MAINTENANCE_START_DATE='YYYY-MM-DD HH:MM:SS' # Optional: For maintenance mode display
```
**Note:** Ensure the `instance` folder exists if using SQLite, or that your PostgreSQL server is running and accessible.

---

## Testing
The project includes a suite of unit tests to ensure code quality and functionality.

### Running Tests
To discover and run all tests, navigate to the root directory of the project and use the following command:
```bash
python -m unittest discover tests
```
This will automatically find and execute all test cases located in the `tests` directory.

---

## Project Status & Maintenance
This project is actively maintained. Dependencies are periodically updated to ensure security and leverage the latest features. Recent updates include key libraries such as Flask, SQLAlchemy, and associated extensions, as well as development tools like linters.

---

## Project Management  
- **Trello**: [Task Tracking](https://trello.com/b/eR2X9dfh)  
- **Live Demo App Running**: [Production Build](https://web-production-d728.up.railway.app/)  
- **Documentation**: See `/STUDI` folder for flowcharts, exam materials, and technical specs.  

---

## Contributions & Licensing  
- **Contributions**: Follow [CONTRIBUTING.md](https://github.com/Kvnbbg/au-garage/CONTRIBUTING.md).  
- **License**: Custom license for commercial/developmental use ([Details](https://github.com/Kvnbbg/au-garage/LICENSE)).  

--- 

![Signature](https://i.imgur.com/wmxtaI7.jpg)  
*Maintained by Kévin Marville | 2025*
