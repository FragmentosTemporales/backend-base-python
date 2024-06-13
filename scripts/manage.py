import logging
import click
from flask.cli import FlaskGroup
from app import create_app
from app.helpers import Installer
from app.models import User


cli = FlaskGroup(create_app=create_app)


@cli.command("create-user")
@click.option("--email", required=True)
@click.option("--password", required=True)
def create_user(email, password):
    """ Create user in the platform by command line interface """
    if User.exists(email):
        print("El usuario ya existe en la base de datos")
    try:
        user = User(password=password, email=email)
        user.set_password(password)
        user.save_to_db()
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en create_user: {error_message}")


@cli.command("install")
def create_data():
    """Create data un the app by comand line"""
    try:
        Installer()
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en installer_app: {error_message}")


@cli.command("test")
@click.option("--test_name")
def test(test_name=None):
    """ Runs the unit tests."""
    import unittest
    if test_name is None:
        tests = unittest.TestLoader().discover('tests', pattern="test_*.py")
    else:
        tests = unittest.TestLoader().loadTestsFromName('tests.' + test_name)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    cli()
