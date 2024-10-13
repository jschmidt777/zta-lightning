import json
import os

from flask import Flask, request, jsonify
import jwt
import datetime

from flask.cli import load_dotenv

from token_verification import token_verification

app = Flask(__name__)

load_dotenv()

# load configuration for the appliance
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret_key")
USE_HTTPS = os.getenv("USE_HTTPS", "False").lower() == "true"
SIMULATION_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(SIMULATION_DIR, "users.json")
# todo: make this configurable to point to two other configs
# there will be three total: compliant, non-compliant, and partial compliant
DEVICES_FILE = os.path.join(SIMULATION_DIR, "configurations.json")

if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)

if os.path.exists(DEVICES_FILE):
    with open(DEVICES_FILE, "r") as f:
        device_configurations = json.load(f)


@app.route("/auth", methods=["POST"])
def authenticate():
    """Authenticate the user.

    :return: a JSON response
    """
    data = request.json
    # password handled this way for simulation simplicity
    username = data.get("username")
    password = data.get("password")
    user = users.get(username)
    if user and user["password"] == password:
        token = jwt.encode(
            {"username": username, "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)},
            JWT_SECRET_KEY,
            algorithm="HS256",
        )

        return jsonify({"token": token}), 200
    return jsonify({"status": "Authentication Failed"}), 401


@app.route("/authorize", methods=["POST"])
@token_verification
def authorize(current_user):
    """Authorize the user.

    :param current_user: the user
    :return: a JSON response
    """
    data = request.json
    resource = data.get("resource")
    # Authorization logic
    if "admin" in current_user["roles"] or resource == "public":
        return jsonify({"status": "Authorized"}), 200
    return jsonify({"status": "Unauthorized"}), 403


@app.route("/device/<hostname>/config", methods=["GET"])
@token_verification
def get_device_configuration(current_user, hostname):
    """Get the device configuration.

    :param current_user: the user
    :param hostname: the hostname of the device
    :return: a JSON response
    """
    if "admin" not in current_user["roles"]:
        return jsonify({"status": "Unauthorized"}), 403

    device_config = device_configurations.get(hostname)
    if device_config:
        return jsonify({"status": "success", "configuration": device_config}), 200
    else:
        return jsonify({"status": "error", "message": "Device not found"}), 404


@app.route("/device/configs", methods=["GET"])
@token_verification
def get_all_device_configurations(current_user):
    """Get all device configuration data.

    :param current_user: the user
    :return: a JSON response
    """
    if "admin" not in current_user["roles"]:
        return jsonify({"status": "Unauthorized"}), 403

    if device_configurations:
        return jsonify({"status": "success", "configurations": device_configurations}), 200
    else:
        return jsonify({"status": "error", "message": "Device configurations not found"}), 404


@app.route("/users/data", methods=["GET"])
@token_verification
def get_all_user_info(current_user):
    """Get all user info data.

    :param current_user: the user
    :return: a JSON response
    """
    if "admin" not in current_user["roles"]:
        return jsonify({"status": "Unauthorized"}), 403

    if users:
        sanitized_users = {
            user: {key: value for key, value in info.items() if key != "password"} for user, info in users.items()
        }
        return jsonify({"status": "success", "users": sanitized_users}), 200
    else:
        return jsonify({"status": "error", "message": "User info. not found"}), 404


if __name__ == "__main__":
    if USE_HTTPS:
        app.run(debug=True, port=443, ssl_context=("appliance.crt", "appliance.key"))
    else:
        app.run(debug=True)
