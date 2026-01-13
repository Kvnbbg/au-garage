# Agent Context: Garage V. Parrot Management System

## Mission Snapshot
A Flask-based garage management platform for service tracking, customer access, and role-based dashboards. The system prioritizes production-ready configuration, secure defaults, and maintainable structure.

## Architectural Topology (High-Level)
- **Backend**: Flask application entrypoints via `run.py` (local) and `api/index.py` (Vercel).
- **Persistence**: SQLAlchemy + Flask-Migrate (SQLite for local, PostgreSQL for production).
- **Security**: CSRF protection, rate limiting, HTTP security headers, and mail-based password reset flows.

## Key Directories
- `app/`: Core Flask application (blueprints, models, services, templates).
- `migrations/`: Database migrations.
- `tests/`: Test suite.
- `api/`: Serverless entrypoint for Vercel.
- `instance/`: Runtime instance data (e.g., local SQLite DB).

## Local Setup & Commands
- Install:
  ```bash
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
- Run locally:
  ```bash
  flask --app run:app run
  # or
  python run.py
  ```
- First-run setup:
  ```bash
  flask garage init-db
  flask garage create-admin
  ```
- Tests:
  ```bash
  pytest
  ```

## Configuration Notes
- Copy `.env.example` → `.env` for local development.
- Required in production: `SECRET_KEY`, `DATABASE_URL`, and a persistent rate limit storage (`RATELIMIT_STORAGE_URI`).
- Vercel deployments use `api/index.py`.

## Contribution Expectations
- Prefer small, focused changes with clear validation steps.
- Update docs when changing workflows or environment requirements.
- Keep security posture intact (CSRF, auth, rate limits, headers).

## Fast Risk Checks (Pre-Change)
- **Secrets**: Avoid committing `.env` or credentials.
- **Auth & Roles**: Verify role-based access remains intact.
- **Migrations**: If models change, ensure migrations exist.
- **Rate Limiting**: Preserve rate-limit configuration and behavior.

