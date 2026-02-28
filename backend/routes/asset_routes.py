from flask import Blueprint, request, jsonify
from app.core.auth import token_required
from app.services.asset_service import create_asset

asset_bp = Blueprint("asset", __name__)


@asset_bp.route("/assets",methods=["POST"])
@token_required
def add_asset(current_user,user_role):
    data=request.get_json()
    domain=data.get("domain")
    ip_address = data.get("ip_address")

    asset_id = create_asset(current_user, domain, ip_address)

    return jsonify({"asset_id": asset_id}),201
#AI
@asset_bp.route("/assets/<int:asset_id>/risk", methods=["GET"])
@token_required
def get_risk_score(current_user, user_role, asset_id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT risk_score FROM scans
        WHERE asset_id=%s
        ORDER BY scan_date DESC
        LIMIT 1
    """, (asset_id,))

    result = cur.fetchone()

    cur.close()
    release_db_connection(conn)

    if not result:
        return jsonify({"risk_score": 0})

    return jsonify({"risk_score": result[0]})


    #AI
    from flask import send_file
from app.services.reporting_service import ReportingService


@asset_bp.route("/report/executive", methods=["GET"])
@token_required
def executive_report(current_user, role):

    file_path = ReportingService.generate_executive_report()

    return send_file(
        file_path,
        as_attachment=True,
        download_name="Executive_Report.pdf",
        mimetype="application/pdf"
    )