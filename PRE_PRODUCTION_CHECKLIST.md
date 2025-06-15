## Pre-Production Checklist

This checklist outlines key considerations before deploying the Garage V. Parrot Management System to a live production environment.

### I. Configuration & Environment
- [ ] **Environment Variables:** Ensure all required environment variables are set and secured in the production environment. Do NOT hardcode secrets.
  - [ ] `SECRET_KEY`: Strong, unique random string.
  - [ ] `DATABASE_URL`: Points to the production PostgreSQL (or other chosen) database.
  - [ ] `FLASK_ENV`: Set to `production`.
  - [ ] `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USE_SSL`, `MAIL_USERNAME`, `MAIL_PASSWORD`: Correctly configured for the production email service.
  - [ ] `MAINTENANCE_START_DATE`: Set if maintenance mode text is used.
  - [ ] (Add any other custom environment variables)
- [ ] **`.env` File:** Ensure the `.env` file is NOT committed to version control if it contains production secrets. Use environment variables directly or a secure secrets management system.
- [ ] **Debug Mode:** Confirm `DEBUG` mode is `False` in production (`FLASK_ENV=production` should handle this).

### II. Database
- [ ] **Production Database:** Separate, robust database instance (e.g., PostgreSQL).
- [ ] **Database Backups:** Regular automated backup schedule configured for the production database.
- [ ] **Migrations:** Run `flask db upgrade` to ensure the database schema is up-to-date with the latest models.
- [ ] **Initial Roles:** Run `flask init-roles` to populate the `roles` table if it's a new database.

### III. Application Deployment & Serving
- [ ] **WSGI Server:** Use a production-grade WSGI server (e.g., Gunicorn, uWSGI). Do not use `flask run`.
  - [ ] Example Gunicorn command: `gunicorn --workers 3 --bind 0.0.0.0:5000 "app:create_app()"` (adjust workers, port as needed).
- [ ] **HTTPS:** Application must be served over HTTPS.
  - [ ] Configure HTTPS at the load balancer, reverse proxy (e.g., Nginx, Caddy), or CDN level.
  - [ ] Ensure `SESSION_COOKIE_SECURE=True` is effectively active.
- [ ] **Static Files:** Configure serving of static files efficiently, typically via a web server like Nginx or a CDN, not directly by Flask in production.
- [ ] **File Permissions:** Ensure correct file permissions for the application code and any directories the app might write to (e.g., instance folder if used for logs or SQLite, though not recommended for production scaling).

### IV. Security
- [ ] **Firewall:** Network firewall configured to only allow necessary inbound traffic (e.g., port 80/443).
- [ ] **Dependencies:** All Python packages in `requirements.txt` are up-to-date and audited for known vulnerabilities.
- [ ] **CSRF Protection:** Verified active on all forms.
- [ ] **Rate Limiting:** Active on sensitive endpoints like login.
- [ ] **Error Handling:** Sensitive error details should not be exposed to users in production.
- [ ] **Regular Security Audits:** Plan for periodic security reviews or penetration testing.

### V. Logging & Monitoring
- [ ] **Logging:** Configure comprehensive logging.
  - [ ] Log to files or a centralized logging service.
  - [ ] Adjust log levels appropriately for production (e.g., INFO or WARNING).
- [ ] **Monitoring:** Set up application performance monitoring (APM) and uptime monitoring.
  - [ ] Track error rates, response times, resource usage.

### VI. Final Checks
- [ ] **Testing:** All unit and integration tests pass in an environment closely resembling production.
- [ ] **Favicon & Static Assets:** Ensure `favicon.ico` and other essential static assets are in place.
- [ ] **Remove Development Tools:** Ensure any development-specific tools or debug routes are disabled or removed.
- [ ] **Review README:** Ensure `README.md` is up-to-date with deployment notes if necessary.
