
from flask import Blueprint, render_template
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager
)
from app.schemas import UserSchema, UserInfoSchema


main = Blueprint("main", __name__)
jwt = JWTManager()
cors = CORS(resources={r"/*": {"origins": "*"}})


user_schema = UserSchema()
user_info_schema = UserInfoSchema()


@main.route("/")
def home():
    """ Home function """
    return render_template('index.html'), 200

