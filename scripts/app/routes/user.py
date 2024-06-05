import logging
from flask import Blueprint, jsonify, request, render_template
from flask_cors import CORS
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    JWTManager
)
from app.models import User
from app.schemas import UserSchema, UserInfoSchema


user = Blueprint("user", __name__)
jwt = JWTManager()
cors = CORS(resources={r"/*": {"origins": "*"}})


user_schema = UserSchema()
user_info_schema = UserInfoSchema()


@user.route("/user")
@jwt_required()
def get_user():
    """Retorna la información del usuario según su ID"""
    try:
        uid = get_jwt_identity()
        user = User.find_by_email(uid)
        if user:

            return jsonify(user_schema.dump(user))

        return jsonify(f"Usuario no encontrado."), 404

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@user.route("/userlist", methods=["PUT", "DELETE"])
@jwt_required()
def update_user():
    """Recibe parámetros para actualizar o deshabilitar al usuario"""
    try:
        uid = get_jwt_identity()
        user = User.find_by_email(uid)
        if user is None:
            return jsonify(f"Usuario no encontrado."), 404
        if request.method == "DELETE":
            user.is_disabled = True
            user.save_to_db()
            return jsonify("USUARIO DESHABILITADO"), 204
        args_json = request.get_json()
        try:
            user.update(**args_json)
            return jsonify("Usuario Actualizado"), 200
        except Exception as e:
            print (e)
            raise e
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

