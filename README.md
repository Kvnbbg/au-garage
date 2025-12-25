# Garage V. Parrot Management System

A Flask-based garage management platform for service tracking, customer access, and role-based dashboards. This repository focuses on a production-ready Python service with clear configuration, reliable startup flows, and maintainable structure.

## Product Scope
- **Service Operations**: Track vehicle repairs, maintenance, and service history.
- **Role-Based Experience**: Admin, Maintenance, Worker, and Client dashboards.
- **Customer Access**: Registration, login, and profile management.
- **Operational Visibility**: Maintenance status messaging, visit leaderboard, and activity logging.

## Tech Stack (Primary Language: Python)
- **Backend**: Flask, Flask-Login, Flask-WTF, Flask-Mail
- **Database**: SQLAlchemy + Flask-Migrate (SQLite for local dev; PostgreSQL for production)
- **Security**: CSRF protection, rate limiting, HTTP security headers

## Prerequisites
- Python 3.10+
- pip
- SQLite (local) or PostgreSQL (production)

## Install
```bash
git clone https://github.com/Kvnbbg/au-garage
cd au-garage
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration
Copy the example environment file and adjust as needed:
```bash
cp .env.example .env
```

Key environment variables:
- `FLASK_ENV` (`development`, `testing`, `production`)
- `SECRET_KEY` (required in production)
- `DATABASE_URL` (e.g. `sqlite:///instance/app.db` or PostgreSQL URL)
- `MAINTENANCE_START_DATE` (format `YYYY-MM-DD HH:MM:SS`)
- `RATELIMIT_STORAGE_URI` (defaults to in-memory for local use)
- `MAIL_*` values for password reset emails
- `ADMINS` (comma-separated list of admin emails)

## Run
### Local development
```bash
flask --app run:app run
```

### Alternate entrypoint
```bash
python run.py
```

## First-Run Setup
```bash
flask garage init-db
flask garage create-admin
```

## CLI Usage Examples
```bash
flask garage --help
flask garage init-roles
flask garage config-check
```

## Web Routes (Examples)
- `/` or `/home`: landing page
- `/auth/login`: login
- `/auth/register`: register
- `/auth/dashboard`: dashboard

## Testing
```bash
pytest
```

## Troubleshooting
- **Database errors**: verify `DATABASE_URL` is correct and migrations ran.
- **Email not sending**: confirm `MAIL_SERVER`, `MAIL_USERNAME`, and `MAIL_PASSWORD`.
- **Rate limit responses**: slow down requests or adjust limits in `app/__init__.py`.
- **Config warnings on startup**: run `flask garage config-check` for details.

## Security Notes
- Set a strong `SECRET_KEY` in production.
- Use a real SMTP provider for email flows.
- Keep dependencies updated and review `SECURITY.md` for reporting.

## Contribution Workflow
1. Fork the repository and create a feature branch.
2. Run tests and lint checks locally.
3. Submit a PR with clear scope and validation steps.

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidance.

## License
[MIT](LICENSE)
