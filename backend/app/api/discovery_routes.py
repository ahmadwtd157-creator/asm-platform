from flask import Blueprint, jsonify
from app.core.auth import token_required
from app.services.discovery_service import discover_subdomains
from app.services.db_service import get_db_connection

discovery_bp = Blueprint("discovery", __name__)

@discovery_bp.route("/discover/<int:asset_id>", methods=["POST"])
@token_required
def discover(current_user, user_role, asset_id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT domain FROM assets WHERE id=%s AND user_id=%s;",
        (asset_id, current_user)
    )

    asset = cur.fetchone()

    cur.close()
    conn.close()

    if not asset:
        return jsonify({
            "message": "Asset not found or access denied"
        }), 404

    domain = asset[0]

    if not domain:
        return jsonify({
            "message": "Asset has no domain"
        }), 400

    try:
        new_subdomains = discover_subdomains(asset_id, domain)

        return jsonify({
            "discovered": len(new_subdomains),
            "new_subdomains": new_subdomains
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Discovery failed",
            "error": str(e)
        }), 500