from functools import wraps
from flask import request, jsonify
import jwt
import os
from app.core.config import JWT_SECRET

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            parts = auth_header.split(" ")

            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            data = jwt.decode(token,JWT_SECRET, algorithms=["HS256"])
            current_user = data.get("user_id")
            user_role = data.get("role")
        except Exception:
            return jsonify({"message": "Token is invalid"}), 401

        return f(current_user, user_role, *args, **kwargs)

    return decorated

def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated(current_user, user_role, *args, **kwargs):
            if user_role not in roles:
                return jsonify({'message':'no access for your role'}), 403
            return f(current_user, user_role, *args, **kwargs)
        return decorated
    return wrapper

    
