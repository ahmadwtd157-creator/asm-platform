#AI
from flask import Blueprint, jsonify
from app.services.dashboard_service import DashboardService
from app.core.auth import token_required

dashboard_bp = Blueprint("dashboard_bp", __name__)


@dashboard_bp.route("/dashboard/summary", methods=["GET"])
@token_required
def dashboard_summary(current_user, user_role):

    data = DashboardService.get_summary()

    return jsonify(data), 200
