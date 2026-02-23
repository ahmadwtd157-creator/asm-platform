from flask import Blueprint, request, jsonify
from app.core.auth import token_required
from app.services.asset_service import create_asset

asset_bp = Blueprint("asset", __name__)


@asset_bp.route("/assets",methods=["POST"])
@token_required
def add_asset(current_user,usre_role):
    data=request.get_json()
    domain=data.get("domain")
    ip_address = data.get("ip_address")

    asset_id = create_asset(current_user, domain, ip_address)

    return jsonify({"asset_id": asset_id}),201