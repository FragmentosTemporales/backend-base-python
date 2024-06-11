import logging
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    JWTManager
)
from app.models import User, Client
from app.schemas import ClientSchema


client = Blueprint("client", __name__)
jwt = JWTManager()
cors = CORS(resources={r"/*": {"origins": "*"}})

client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)


@client.route("/create-client", methods=["POST"])
@jwt_required()
def create_client():
    """Recibe parámetros a través de la consulta y crea el cliente."""
    try:
        args_json = request.get_json()
        if not args_json:
            return jsonify({"error": "No input data provided"}), 400

        uid = get_jwt_identity()
        user = User.find_by_email(uid)

        if not user:
            return jsonify({"error": "User not found"}), 404

        try:
            args = client_schema.load(args_json)

        except Exception as e:
            return jsonify({"error": "Error processing request", "message": str(e)}), 500

        rut = args["rut"]

        client = Client(**args)
        client.set_rut(rut)
        client.user_id = user.id
        client.save_to_db()

        return jsonify({"message": "Client info created successfully!"}), 201

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@client.route("/clientlist", methods=["GET"])
@jwt_required()
def get_user_info():
    """Retorna la información del usuario según su ID"""
    try:
        uid = get_jwt_identity()
        user = User.find_by_email(uid)
        clientlist = Client.find_by_user_id(user.id)
        if user:

            if not clientlist:

                return jsonify(f"Información no encontrada."), 404

            client_data = clients_schema.dump(clientlist)
            return jsonify(client_data), 200

        return jsonify("Usuario no encontrado."), 404

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@client.route("/client-info/<int:client_id>", methods=["GET"])
@jwt_required()
def get_client_info(client_id):
    """Retorna la información del cliente según su ID y verifica que pertenece al usuario"""
    try:
        uid = get_jwt_identity()
        user = User.find_by_email(uid)

        if not user:
            return jsonify({"error": "Usuario no encontrado."}), 404

        clientlist = Client.find_by_user_id(user.id)

        if not clientlist:
            return jsonify({"error": "Información no encontrada."}), 404

        client = next((c for c in clientlist if c.id == client_id), None)

        if not client:
            return jsonify({"error": "Cliente no encontrado o no pertenece al usuario."}), 404

        client_data = client_schema.dump(client)

        return jsonify(client_data), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@client.route("/update-client/<int:client_id>", methods=["PUT", "DELETE"])
@jwt_required()
def update_user(client_id):
    """Recibe parámetros para actualizar o deshabilitar al cliente"""
    try:
        uid = get_jwt_identity()
        user = User.find_by_email(uid)
        if user is None:
            return jsonify({"error": "Usuario no encontrado."}), 404

        clientlist = Client.find_by_user_id(user.id)
        if not clientlist:
            return jsonify({"error": "Información no encontrada."}), 404

        client = next((c for c in clientlist if c.id == client_id), None)
        if not client:
            return jsonify({"error": "Cliente no encontrado."}), 404

        if request.method == "DELETE":
            return disable_client(client)
        elif request.method == "PUT":
            return update_client_info(client)

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

def disable_client(client):
    try:
        client.is_disabled = True
        client.save_to_db()
        return jsonify({"message": "Client info updated successfully!"}), 204
    except Exception as e:
        return jsonify({"error": "Failed to disable client", "message": str(e)}), 500

def update_client_info(client):
    try:
        args_json = request.get_json()
        if 'rut' in args_json:
            args_json['rut'] = args_json['rut'].replace('.', '').replace('-', '').lower()
        client.update(**args_json)
        return jsonify({"message": "Client info updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to update client info", "message": str(e)}), 500
