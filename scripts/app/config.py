import os
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """ Base configuration application class """
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_HOURS"))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_DAYS"))
    )
    SECRET_KEY = os.environ.get("SECRET_KEY")


class DevConfig(BaseConfig):
    """ Development configuration class """
    db_user = os.environ.get("POSTGRES_USER")
    db_pass = os.environ.get("POSTGRES_PASSWORD")
    db_name = os.environ.get("POSTGRES_DB")
    db_host = os.environ.get("POSTGRES_HOST")
    db_port = os.environ.get("POSTGRES_PORT")
    SQLALCHEMY_DATABASE_URI = ("postgresql://{}:{}@{}:{}/{}".format(
        db_user, db_pass, db_host, db_port, db_name
    ))


class TestConfig(BaseConfig):
    """ Testing configuration class """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, "..", 'test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    "dev": DevConfig,
    "test": TestConfig
}
