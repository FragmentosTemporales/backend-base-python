import logging
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    JWTManager
)
from app.models import User, UserInfo
from app.schemas import UserSchema, UserInfoSchema


user_info = Blueprint("user_info", __name__)
jwt = JWTManager()
cors = CORS(resources={r"/*": {"origins": "*"}})


user_schema = UserSchema()
user_info_schema = UserInfoSchema()


@user_info.route("/set/user-info", methods=["POST"])
@jwt_required()
def create_user_info():
    """Recibe parámetros a través de la consulta y crea la información de usuario."""
    try:
        args_json = request.get_json()
        if not args_json:
            return jsonify({"error": "No input data provided"}), 400

        uid = get_jwt_identity()
        user = User.find_by_email(uid)
        
        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.user_info:
            print("Información ya existe")
            return jsonify({"error": "User info already exists"}), 400

        try:
            args = user_info_schema.load(args_json)

        except Exception as e:
            return jsonify({"error": "Error processing request", "message": str(e)}), 500

        first_name = args["first_name"]
        last_name = args["last_name"]

        user_info = UserInfo(**args)
        user_info.set_names(first_name, last_name)
        user_info.user_id = user.id
        user_info.save_to_db()

        return jsonify({"message": "User info created successfully!"}), 201

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@user_info.route("/user-info")
@jwt_required()
def get_user_info():
    """Retorna la información del usuario según su ID"""
    try:
        uid = get_jwt_identity()
        user = User.find_by_email(uid)
        user_info = UserInfo.find_by_user_id(user.id)
        if user:

            if not user_info:

                return jsonify(f"Información no encontrada."), 404

            return jsonify(user_info_schema.dump(user_info))

        return jsonify(f"Usuario no encontrado."), 404

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@user_info.route("/update-user-info", methods=["PUT", "DELETE"])
@jwt_required()
def update_user_info():
    """Recibe parámetros para actualizar o eliminar información"""
    try:
        uid = get_jwt_identity()
        user = User.find_by_email(uid)
        if user is None:
            return jsonify(f"Usuario no encontrado."), 404
        
        user_info = UserInfo.find_by_user_id(user.id)
        if user_info is None:
            return jsonify(f"Datos no encontrados."), 404

        if request.method == "DELETE":
            user_info.delete_from_db()
            return jsonify("Datos Eliminados"), 204
        args_json = request.get_json()
        try:
            user_info.update(**args_json)
            return jsonify("Información Actualizada"), 200
        except Exception as e:
            print (e)
            raise e

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
