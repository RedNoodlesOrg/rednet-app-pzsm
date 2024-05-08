"""mod.py."""

from __future__ import annotations

from sqlalchemy import Boolean, Column, ForeignKey, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from SteamAPI.mod import Mod, ModId

Base = declarative_base()


class SQLModID(Base):
    """ModID."""

    __tablename__ = "mod_ids"
    workshop_id = Column(String, ForeignKey("mods.workshop_id"), primary_key=True)
    mod_id = Column(String, primary_key=True)
    enabled = Column(Boolean, default=False)

    @staticmethod
    def from_steam(mod_id: ModId, workshop_id: str) -> SQLModID:
        """Create SQLModID from steam mod.

        Args:
            mod_id (ModId): Steam ModId
            workshop_id (str): Steam WorkshopId

        Returns:
            SQLModID: The SQLModID
        """
        sqlmod_id = SQLModID()
        sqlmod_id.workshop_id = workshop_id
        sqlmod_id.mod_id = mod_id.id
        sqlmod_id.enabled = mod_id.enabled
        return sqlmod_id


class SQLMod(Base):
    """Mod."""

    __tablename__ = "mods"
    workshop_id = Column(String, primary_key=True)
    thumbnail = Column(String)
    name = Column(String)
    mod_ids = relationship("SQLModID", backref="mod")

    @staticmethod
    def from_steam(mod: Mod):
        """Create SQLMod from Mod.

        Args:
            mod (Mod): Mod to convert

        Returns:
            _type_: Converted Mod
        """
        sqlmod = SQLMod()
        sqlmod.name = mod.name
        sqlmod.thumbnail = mod.thumbnail
        sqlmod.workshop_id = mod.workshop_id
        mod_ids = []
        for mod_id in mod.mod_ids:
            mod_ids.append(SQLModID.from_steam(mod_id, mod.workshop_id))
        sqlmod.mod_ids = mod_ids
        return sqlmod


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
                    mod_id.enabled = existing_mod_id.enabled
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
