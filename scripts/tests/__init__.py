from flask_testing import TestCase
from app import create_app
from app.models import db


class BaseTestCase(TestCase):
    """ Base Tests """
    def create_app(self):
        app = create_app(test_mode=True)
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
