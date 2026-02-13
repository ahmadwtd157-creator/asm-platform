from flask import Blueprint, request, jsonify
from app.core.auth import roles_required, token_required
import bcrypt
import jwt
import os
from app.services.db_service import get_db_connection

user_bp = Blueprint('user_bp',__name__)

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")

@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    password_hash=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (email, password_hash) VALUES (%s,%s) RETURNING id;",
        (email,password_hash)
    )
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": f"User created with id {user_id}"}), 201

@user_bp.route("/login",methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash, role FROM users WHERE email=%s;"), (email())
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'),user[1].encode('utf-8')):
        payload = {"user_id": user[0], "role": user[2]}
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"token":token})
    else:
        return jsonify({"message": "Invalid credentials"}),401

@user_bp.route("/profile", methods=["GET"])
@token_required
def profile(current_user, user_role):
    return jsonify({"user_id":current_user, "role": user_role})
