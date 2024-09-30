import json
import os
from functools import wraps

import jwt
from flask import request, jsonify
from flask.cli import load_dotenv

SIMULATION_DIR = os.path.dirname(os.path.abspath(__file__))

USERS_FILE = os.path.join(SIMULATION_DIR, "users.json")

if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret_key")


def token_verification(f):
    """Verify that the JWT is valid from the request.

    :param f: the called endpoint
    :return: A JSON response
    """

    @wraps(f)
    def decorator(*args, **kwargs):
        """Decorate the function."""
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            current_user = users.get(data["username"])
            if not current_user:
                return jsonify({"message": "User not found!"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 401

        return f(current_user, *args, **kwargs)

    return decorator
