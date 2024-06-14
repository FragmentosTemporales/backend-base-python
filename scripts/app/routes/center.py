import logging
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    JWTManager
)
from app.models import User, Client, Center
from app.schemas import ClientSchema, CenterSchema


center = Blueprint("center", __name__)
jwt = JWTManager()
cors = CORS(resources={r"/*": {"origins": "*"}})

client_schema = ClientSchema()
center_schema = CenterSchema()
centers_schema = CenterSchema(many=True)


@center.route("/create-center", methods=["POST"])
@jwt_required()
def create_center():
    """Recibe parámetros a través de la consulta y crea el centro."""
    try:
        args_json = request.get_json()
        if not args_json:
            return jsonify({"error": "No input data provided"}), 400

        uid = get_jwt_identity()
        user = User.find_by_email(uid)
        if not user:
            return jsonify({"error": "User not found"}), 404

        try:
            args = center_schema.load(args_json)
        except Exception as e:
            return jsonify({"error": "Error processing request", "message": str(e)}), 400

        client_id = args["client_id"]
        c_workers = args["n_works"]

        client = Client.find_by_id(client_id)
        if not client:
            return jsonify({"error": "Client not found"}), 404

        client_workers = client.n_works
        new_workers = c_workers + client_workers

        try:
            client.n_works = new_workers
            client.update()
        except Exception as e:
            return jsonify({"error": "Error updating client", "message": str(e)}), 500
        center = Center(**args)
        center.save_to_db()

        return jsonify({"message": "Center created successfully!"}), 201

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@center.route("/centerlist/<int:client_id>", methods=["GET"])
@jwt_required()
def get_center_list(client_id):
    """Retorna la información de centros asociados"""
    try:
        uid = get_jwt_identity()
        user = User.find_by_email(uid)
        if not user:
            return jsonify({"error": "User not found"}), 404

        clientlist = Client.find_by_user_id(user.id)

        if not clientlist:
            return jsonify({"error": "Información no encontrada."}), 404

        client = next((c for c in clientlist if c.id == client_id), None)

        if not client:
            return jsonify({"error": "Cliente no encontrado."}), 404
        
        center_data = Center.find_by_client_id(client.id)

        center_list = centers_schema.dump(center_data)

        print("Lista de centros: ",center_list)

        return jsonify(center_list), 200


    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500