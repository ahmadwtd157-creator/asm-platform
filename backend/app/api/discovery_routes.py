from flask import Blueprint, jsonify
from app.core.auth import token_required
from app.services.db_service import discover_subdomains
from app.services.scan_service import asset_belongs_to_user

discovery_bp = Blueprint("discovery", __name__)


@discovery_bp.route("/discover/<int:asset_id>", methods=["POST"])
@token_required
def discover(current_user, user_role,asset_id):

    if not asset_belongs_to_user(asset_id,current_user):
        return jsonify({"message":"Asset not found or access denied"}), 404

    from app.services.db_service import get_db_connection
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT domain FROM assets WHERE id=%s;",(asset_id,))
    asset = cur.fetchone()
    cur.close()
    conn.close()

    if not asset or not asset[0]:
        return jsonify({"message":"Asset has no domain"}), 400

    domain = asset[0]

    new_subdomains = discover_subdomains(asset_id, domain)

    return jsonify({
        "discovered": len(new_subdomains),
        "new_subdomains": new_subdomains

    }), 200
    