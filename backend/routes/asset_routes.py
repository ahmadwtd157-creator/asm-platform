from flask import Blueprint, request, jsonify, send_file
from app.core.auth import token_required
from app.services.asset_service import create_asset
from app.services.db_service import get_db_connection
from app.services.monitoring_service import MonitoringService
from app.services.reporting_service import ReportingService
from app.core.limiter import limiter

asset_bp = Blueprint("asset", __name__)


@asset_bp.route("/assets", methods=["POST"])
@token_required
def add_asset(current_user, user_role):

    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid request body"}), 400

    domain = data.get("domain")
    ip_address = data.get("ip_address")

    if not domain and not ip_address:
        return jsonify({"message": "domain or ip_address required"}), 400

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
        ORDER BY created_at DESC
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


@asset_bp.route("/assets/<int:asset_id>/results", methods=["GET"])
@token_required
def get_asset_results(current_user, user_role, asset_id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id FROM assets
        WHERE id=%s AND user_id=%s
    """, (asset_id, current_user))

    asset = cur.fetchone()

    if not asset:
        cur.close()
        conn.close()
        return jsonify({"message": "Asset not found"}), 404

    cur.execute("""
        SELECT id, risk_score, created_at
        FROM scans
        WHERE asset_id=%s
        ORDER BY created_at DESC
        LIMIT 1
    """, (asset_id,))

    scan = cur.fetchone()

    if not scan:
        cur.close()
        conn.close()
        return jsonify([]), 200

    scan_id = scan[0]
    risk_score = scan[1]
    scan_date = scan[2]

    cur.execute("""
        SELECT port, service, banner, asset_type, category, criticality
        FROM scan_results
        WHERE scan_id=%s AND is_open=TRUE
        ORDER BY port
    """, (scan_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    results = []

    for row in rows:
        results.append({
            "port": row[0],
            "service": row[1],
            "banner": row[2],
            "asset_type": row[3],
            "category": row[4],
            "criticality": row[5],
            "risk_score": risk_score,
            "scan_date": scan_date
        })

    return jsonify(results), 200


@asset_bp.route("/assets/<int:asset_id>/scan", methods=["POST"])
@token_required
@limiter.limit("10 per minute")
def trigger_scan(current_user, user_role, asset_id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT ip_address
    FROM assets
    WHERE id=%s AND user_id=%s
    """, (asset_id, current_user))

    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return jsonify({"message": "Asset not found"}), 404

    ip_address = row[0]

    if not ip_address:

        cur.close()
        conn.close()

        return jsonify({
            "message": "Asset has no IP. Run discovery or resolve DNS first."
        }), 400

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

@asset_bp.route("/assets/<int:asset_id>", methods=["DELETE"])
@token_required
def delete_asset(current_user, user_role, asset_id):

    conn = get_db_connection()
    cur = conn.cursor()

    try:

        # تأكد أن الأصل يخص المستخدم
        cur.execute("""
            SELECT id FROM assets
            WHERE id=%s AND user_id=%s
        """,(asset_id,current_user))

        asset = cur.fetchone()

        if not asset:

            cur.close()
            conn.close()

            return jsonify({"message":"Asset not found"}),404


        # حذف النتائج المرتبطة أولاً (منع مشاكل FK)
        cur.execute("""
            DELETE FROM scan_results
            WHERE scan_id IN (
                SELECT id FROM scans WHERE asset_id=%s
            )
        """,(asset_id,))


        cur.execute("""
            DELETE FROM scans
            WHERE asset_id=%s
        """,(asset_id,))


        # حذف الأصل
        cur.execute("""
            DELETE FROM assets
            WHERE id=%s AND user_id=%s
        """,(asset_id,current_user))


        conn.commit()

        return jsonify({"message":"Asset deleted"}),200

    except Exception as e:

        conn.rollback()

        return jsonify({"message":str(e)}),500

    finally:

        cur.close()
        conn.close()