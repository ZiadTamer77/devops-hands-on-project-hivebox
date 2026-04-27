from flask import Blueprint, jsonify
from app.services.version_service import get_version

version_bp = Blueprint("version", __name__)


@version_bp.route("/version", methods=["GET"])
def version():
    return jsonify({"version": get_version()})
