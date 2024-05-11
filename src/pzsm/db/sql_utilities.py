"""mod.py."""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from SteamAPI.mod import Mod

from .sql_mod import SQLMod
from .sql_mod_id import SQLModID

Base = declarative_base()


def sync(mods: list[Mod]):
    """sync."""
    engine = create_engine("sqlite:///mods.db")
    session_class = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = session_class()

    for mod in mods:
        existing_mod = session.query(SQLMod).filter_by(workshop_id=mod.workshop_id).first()
        if existing_mod:
            existing_mod.thumbnail = mod.thumbnail
            existing_mod.name = mod.name
            for mod_id in mod.mod_ids:
                existing_mod_id = (
                    session.query(SQLModID).filter_by(workshop_id=mod.workshop_id, mod_id=mod_id.id).first()
                )
                if existing_mod_id:
                    mod_id.enabled = existing_mod_id.enabled is not None and existing_mod_id.enabled
                else:
                    existing_mod.mod_ids.append(SQLModID.from_steam(mod_id, mod.workshop_id))
        else:
            sqlmod = SQLMod.from_steam(mod)
            session.add(sqlmod)

    session.commit()


def update_enabled(workshop_id: str, mod_id: str, enabled: bool):
    """update_enabled."""
    engine = create_engine("sqlite:///mods.db")
    session_class = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = session_class()
    existing_mod_id = session.query(SQLModID).filter_by(workshop_id=workshop_id, mod_id=mod_id).first()
    if existing_mod_id:
        existing_mod_id.enabled = enabled
        session.commit()
        return True
    return False
