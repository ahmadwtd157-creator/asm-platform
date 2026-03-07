from flask import Blueprint, request, jsonify, send_file
from app.core.auth import token_required
from app.services.asset_service import create_asset
from app.services.db_service import get_db_connection
from app.services.monitoring_service import MonitoringService
from app.services.reporting_service import ReportingService

asset_bp = Blueprint("asset", __name__)



@asset_bp.route("/assets", methods=["POST"])
@token_required
def add_asset(current_user, user_role):
    data = request.get_json()
    domain = data.get("domain")
    ip_address = data.get("ip_address")

    asset_id = create_asset(current_user, domain, ip_address)

    return jsonify({"asset_id": asset_id}), 201



@asset_bp.route("/assets", methods=["GET"])
@token_required
def get_assets(current_user, user_role):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, domain, ip_address, created_at
        FROM assets
        WHERE user_id=%s
        ORDER BY created_at DESC;
    """, (current_user,))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    assets = []
    for row in rows:
        assets.append({
            "id": row[0],
            "domain": row[1],
            "ip_address": row[2],
            "created_at": row[3]
        })

    return jsonify(assets), 200



@asset_bp.route("/assets/<int:asset_id>", methods=["GET"])
@token_required
def get_asset(current_user, user_role, asset_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, domain, ip_address, created_at
        FROM assets
        WHERE id=%s AND user_id=%s;
    """, (asset_id, current_user))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return jsonify({"message": "Asset not found"}), 404

    return jsonify({
        "id": row[0],
        "domain": row[1],
        "ip_address": row[2],
        "created_at": row[3]
    }), 200



@asset_bp.route("/assets/<int:asset_id>", methods=["DELETE"])
@token_required
def delete_asset(current_user, user_role, asset_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM assets
        WHERE id=%s AND user_id=%s
        RETURNING id;
    """, (asset_id, current_user))

    deleted = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if not deleted:
        return jsonify({"message": "Asset not found"}), 404

    return jsonify({"message": "Asset deleted"}), 200



@asset_bp.route("/assets/<int:asset_id>/results", methods=["GET"])
@token_required
def get_asset_results(current_user, user_role, asset_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT sr.port, sr.service, sr.banner, sr.is_open, s.risk_score, s.created_at
        FROM scan_results sr
        JOIN scans s ON sr.scan_id = s.id
        JOIN assets a ON a.id = s.asset_id
        WHERE s.asset_id=%s AND a.user_id=%s
        ORDER BY s.created_at DESC;
        
    """, (asset_id,current_user))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "port": row[0],
            "service": row[1],
            "banner": row[2],
            "is_open": row[3],
            "risk_score": row[4],
            "scan_date": row[5]
        })

    return jsonify(results), 200



@asset_bp.route("/assets/<int:asset_id>/scan", methods=["POST"])
@token_required
def trigger_scan(current_user, user_role, asset_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT ip_address
        FROM assets
        WHERE id=%s AND user_id=%s;
    """, (asset_id, current_user))

    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return jsonify({"message": "Asset not found"}), 404

    ip_address = row[0]

    MonitoringService.scan_and_compare(asset_id, ip_address, conn)

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Scan completed"}), 200



@asset_bp.route("/report/executive", methods=["GET"])
@token_required
def executive_report(current_user, user_role):
    file_path = ReportingService.generate_executive_report()

    return send_file(
        file_path,
        as_attachment=True,
        download_name="Executive_Report.pdf",
        mimetype="application/pdf"
    )