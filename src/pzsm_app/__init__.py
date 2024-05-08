"""__init__.py."""

from __future__ import annotations

from flask import Flask

from pzsm_app.config import CurrentConfig
from pzsm_app.routes import blueprint


def create_app():
    """create_app."""
    app = Flask(__name__)
    app.config.from_object(CurrentConfig())
    app.register_blueprint(blueprint)
    return app
