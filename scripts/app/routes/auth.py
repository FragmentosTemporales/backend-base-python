import logging
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import (
    create_access_token,
    JWTManager
)
from app.models import User
from app.schemas import UserSchema, LoginSchema


auth = Blueprint('auth', __name__)
jwt = JWTManager()
cors = CORS(resources={r"/*": {"origins": "*"}})


user_schema = UserSchema()
login_schema = LoginSchema()


@auth.route("/register", methods=["POST"])
def create_user():
    """Recibe parámetros a través de la consulta y crea el usuario."""
    try:
        args_json = request.get_json()
        try:
            args = user_schema.load(args_json)
        except Exception as e:
            print(e)
            raise e
        else:
            email = args["email"]
            password = args["password"]
            lower_email = User.set_email_lower
            user_exists = User.exists(lower_email)

            if user_exists:
                return jsonify("Usuario ya existe"), 400

            user = User(**args)
            user.set_password(password)
            user.set_email_lower(email)
            user.save_to_db()
            return jsonify("Usuario creado con éxito!"), 201

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@auth.route("/login", methods=["POST"])
def login_user():
    """Recibe parámetros a través de la consulta y retorna un token"""
    try:
        args_json = request.get_json()
        try:
            args = login_schema.load(args_json)
        except Exception as e:
            print(e)
            raise e
        else:
            email = args["email"]
            password = args["password"]
            user = User.find_by_email(email)

            if user is None or \
               user.check_password(password) == False:
                return jsonify("ERROR DE USUARIO O CONTRASEÑA"), 400

            access_token = create_access_token(email)
            user.is_disabled = False
            user.save_to_db()

            return jsonify(
                    {
                        "token": access_token,
                        "user": user_schema.dump(user),
                        "email": user.email,
                        "user_id": user.id,
                    }
            ), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

