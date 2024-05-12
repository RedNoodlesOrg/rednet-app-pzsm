from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


class EngineSingleton:
    _instance = None

    @staticmethod
    def get_instance() -> Engine:
        if EngineSingleton._instance is None:
            EngineSingleton._instance = create_engine("sqlite:///mods.db")
        return EngineSingleton._instance
