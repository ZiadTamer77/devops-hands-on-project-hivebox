from flask import Flask
from app.routes.version import version_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(version_bp)

    return app
