from flask import Blueprint, request, jsonify
from models import User
from extensions import db, bcrypt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": False, "message": "❌ User not found!"}), 400

    if bcrypt.check_password_hash(user.password, password):
        return jsonify({
            "success": True,
            "message": "✅ Login successful!",
            "user_id": user.id,
            "role": user.role
        }), 200
    else:
        return jsonify({"success": False, "message": "❌ Incorrect password"}), 401
