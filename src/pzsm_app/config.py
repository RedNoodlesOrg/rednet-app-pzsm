"""Edited by Fakeapate."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Config:
    """Config."""

    basedir = os.path.abspath(os.path.dirname(__file__))
    ASSETS_ROOT = os.getenv("ASSETS_ROOT", "/static/assets")
    RCON_PW = os.getenv("RCON_PW", "")
    RCON_HOST = os.getenv("RCON_HOST", "")
    RCON_PORT = os.getenv("RCON_PORT", "27015")
    COLLECTION_ID = os.getenv("COLLECTION_ID", "3126799274")
    PZ_SERVER_FOLDER = os.getenv("PZ_SERVER_FOLDER", "")
    DOCKER_URL = os.getenv("DOCKER_URL", "unix://var/run/docker.sock")
    DOCKER_CONTAINER = os.getenv("DOCKER_CONTAINER", "pzserver_node_1")


@dataclass
class ProductionConfig(Config):
    """ProductionConfig."""

    DEBUG = False
    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600


@dataclass
class DebugConfig(Config):
    """DebugConfig."""

    DEBUG = True


@dataclass
class CurrentConfig(DebugConfig):
    """CurrentConfig."""
