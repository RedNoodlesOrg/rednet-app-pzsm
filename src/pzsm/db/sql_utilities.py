"""mod.py."""

from __future__ import annotations

from sqlalchemy.orm import Session

from SteamAPI.mod import Mod

from .sql_base import SQLBase
from .sql_engine import EngineSingleton
from .sql_mod import SQLMod
from .sql_mod_id import SQLModID


def sync(mods: list[Mod]) -> None:
    """sync."""
    engine = EngineSingleton.get_instance()
    SQLBase.metadata.create_all(engine)
    with Session(engine) as session:
        with session.begin():
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


def update_enabled(workshop_id: str, mod_id: str, enabled: bool) -> bool:
    """update_enabled."""
    result = False
    engine = EngineSingleton.get_instance()
    SQLBase.metadata.create_all(engine)
    with Session(engine) as session:
        with session.begin():
            existing_mod_id = session.query(SQLModID).filter_by(workshop_id=workshop_id, mod_id=mod_id).first()
            if existing_mod_id:
                existing_mod_id.enabled = enabled
                result = True
    return result
