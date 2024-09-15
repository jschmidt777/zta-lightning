import json
import os

from flask import Flask, request, jsonify
import jwt
import datetime

from flask.cli import load_dotenv

from token_verification import token_verification

app = Flask(__name__)

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret_key")

SIMULATION_DIR = os.path.dirname(os.path.abspath(__file__))

USERS_FILE = os.path.join(SIMULATION_DIR, "users.json")
DEVICES_FILE = os.path.join(SIMULATION_DIR, "configurations.json")


if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)


if os.path.exists(DEVICES_FILE):
    with open(DEVICES_FILE, "r") as f:
        devices_configurations = json.load(f)


@app.route("/auth", methods=["POST"])
def authenticate():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    user = users.get(username)
    if user and user["password"] == password:
        token = jwt.encode(
            {"username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            JWT_SECRET_KEY,
            algorithm="HS256",
        )

        return jsonify({"token": token}), 200
    return jsonify({"status": "Authentication Failed"}), 401


@app.route("/authorize", methods=["POST"])
@token_verification
def authorize(current_user):
    data = request.json
    resource = data.get("resource")
    # Authorization logic
    if "admin" in current_user["roles"] or resource == "public":
        return jsonify({"status": "Authorized"}), 200
    return jsonify({"status": "Unauthorized"}), 403


@app.route("/account", methods=["POST"])
@token_verification
def account(current_user):
    data = request.json
    action = data.get("action")
    current_user["usage"].append(action)
    return jsonify({"status": "Logged"}), 200


@app.route("/device/<hostname>/config", methods=["GET"])
@token_verification
def get_device_configuration(current_user, hostname):
    if "admin" not in current_user["roles"]:
        return jsonify({"status": "Unauthorized"}), 403

    device_config = devices_configurations.get(hostname)
    if device_config:
        return jsonify({"status": "success", "configuration": device_config}), 200
    else:
        return jsonify({"status": "error", "message": "Device not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
