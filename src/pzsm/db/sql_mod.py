from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from SteamAPI.mod import Mod

from .sql_base import SQLBase
from .sql_mod_id import SQLModID


class SQLMod(SQLBase):
    """Mod."""

    __tablename__ = "mods"
    workshop_id = mapped_column(String, primary_key=True)
    thumbnail = mapped_column(String)
    name = mapped_column(String)
    mod_ids: Mapped[list[SQLModID]] = relationship("SQLModID", backref="mod")

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
