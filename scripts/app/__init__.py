import os
from flask import Flask
from app.config import config
from app.models import db, migrate
from app.routes.main import cors, jwt, main
from app.routes.auth import auth
from app.routes.user import user
from app.routes.user_info import user_info
from app.routes.client import client


def create_app(test_mode=False):
    """ Create flask application instance """
    app = Flask(__name__)
    if test_mode:
        app.config.from_object(config["test"])
    else:
        env = os.environ.get("FLASK_ENV", "dev")
        app.config.from_object(config[env])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(user_info)
    app.register_blueprint(client)

    return app
