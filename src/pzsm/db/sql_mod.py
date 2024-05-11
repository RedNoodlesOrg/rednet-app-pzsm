from __future__ import annotations

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from SteamAPI.mod import Mod

from .sql_mod_id import SQLModID
from .sql_utilities import Base


class SQLMod(Base):
    """Mod."""

    __tablename__ = "mods"
    workshop_id = Column(String, primary_key=True)
    thumbnail = Column(String)
    name = Column(String)
    mod_ids: list[SQLModID] = relationship("SQLModID", backref="mod", collection_class=list)

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
        mod_ids: list[SQLModID] = []
        for mod_id in mod.mod_ids:
            mod_ids.append(SQLModID.from_steam(mod_id, mod.workshop_id))
        sqlmod.mod_ids = mod_ids
        return sqlmod
