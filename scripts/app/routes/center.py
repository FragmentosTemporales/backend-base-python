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


# TODO = Simplificar validaciones y disminuir cantidad de returns
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
            print(args)

        except Exception as e:
            return jsonify({"error": "Error processing request", "message": str(e)}), 500


        client_id = args["client_id"]
        c_workers = args["n_works"]


        center = Center(**args)
        client = Client.find_by_id(client_id)

        if not client:
            return jsonify({"error": "Client not found"}), 404

        client_workers = client.n_works
        new_workers = c_workers + client_workers

        try:
            client.n_works = new_workers
            client.update(**client)

        except Exception as e:
            return jsonify({"error": "Error processing request", "message": str(e)}), 500

        center.save_to_db()
        print("Creando centro de trabajo...")

        return jsonify({"message": "Client info created successfully!"}), 201

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500