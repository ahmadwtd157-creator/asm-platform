from flask import Blueprint, jsonify
from app.core.auth import roles_required, token_required

admin_bp - Blueprint('admin_bp',__name__)

@admin_bp.route("/admin/projects", methods=[DELETE])
@token_required
@roles_required('admin')
def delete_projects(current_user, user_role):
    return jsonify({"message": "Project deleted"})
    