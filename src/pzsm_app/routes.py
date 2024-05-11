"""
Copyright (c) 2019 - present AppSeed.us.

Edited by Fakeapate
"""

from __future__ import annotations

import os

from flask import Blueprint, jsonify, render_template
from jinja2 import TemplateNotFound

from pzsm.db.mod import sync, update_enabled
from pzsm.docker import restart
from pzsm.file_parser.modlist import Modlist
from pzsm.file_parser.server_settings import ServerSettings
from pzsm_app.config import CurrentConfig
from SteamAPI.collection import Collection

blueprint = Blueprint(
    "views",
    __name__,
)


def base_render(file: str, **kwargs):
    """base_render."""
    try:
        return render_template(file, **kwargs)
    except TemplateNotFound:
        return render_template("home/page-404.html"), 404
    except Exception:
        return render_template("home/page-500.html"), 500


@blueprint.route("/cmd/restart", methods=["POST"])
def cmd_restart():
    """restart."""
    return jsonify(success=restart(CurrentConfig.DOCKER_URL, CurrentConfig.DOCKER_CONTAINER))


@blueprint.route("/cmd/applymods", methods=["POST"])
def cmd_apply_mods():
    """apply_mods."""
    server_settings = ServerSettings(os.path.join(CurrentConfig.PZ_SERVER_FOLDER, "Server/servertest.ini"))
    collection = Collection(CurrentConfig.COLLECTION_ID)
    sync(collection.mods)
    modlist = Modlist(collection.mods)
    server_settings.update_mods(modlist).save()
    return jsonify(success=True)


@blueprint.route("/cmd/update/mod/<string:workshop_id>/<string:mod_id>/<int:enabled>", methods=["POST"])
def cmd_update_enabled(workshop_id: str, mod_id: str, enabled: int):
    """update_enabled."""
    return jsonify(success=update_enabled(workshop_id, mod_id, enabled == 1))


@blueprint.route("/")
@blueprint.route("/index")
@blueprint.route("/index.html")
def pz():
    """pz."""
    mods = Collection(CurrentConfig.COLLECTION_ID).mods
    return base_render("home/mods.html", mods=mods, count_mods=len(mods))


@blueprint.route("/logs")
@blueprint.route("/logs.html")
def logs():
    """Get logs."""
    return base_render("home/logs.html")
