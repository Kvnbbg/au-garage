import click
from flask.cli import with_appcontext

from config import load_config


@click.group(help="Garage V. Parrot management commands.")
def garage():
    pass


@garage.command("init-roles")
@with_appcontext
def init_roles_command():
    """Initialize predefined roles."""
    from app.models import init_roles

    init_roles()
    click.echo("Roles initialized.")


@garage.command("init-db")
@with_appcontext
def init_db():
    """Create database tables and seed roles."""
    from app import db
    from app.models import init_roles

    db.create_all()
    init_roles()
    click.echo("Database tables created and roles seeded.")


@garage.command("create-admin")
@click.option("--username", prompt=True)
@click.option("--email", prompt=True)
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
)
@with_appcontext
def create_admin(username, email, password):
    """Create an admin user for first-run setup."""
    from app import db
    from app.models import Role, User, init_roles

    existing = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existing:
        click.echo("User already exists. Choose another username or email.")
        return
    admin_role = Role.find_by_name("Admin")
    if not admin_role:
        init_roles()
        admin_role = Role.find_by_name("Admin")
    user = User(username=username, email=email.lower().strip(), role_id=admin_role.id)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo(f"Admin user '{username}' created.")


@garage.command("config-check")
def config_check():
    """Validate configuration and print any warnings."""
    _, warnings = load_config()
    if not warnings:
        click.echo("Configuration OK.")
        return
    click.echo("Configuration warnings:")
    for warning in warnings:
        click.echo(f"- {warning}")


def register_cli(app):
    app.cli.add_command(garage)
