from __future__ import annotations

from sqlalchemy import Boolean, Column, ForeignKey, String

from SteamAPI.mod import ModId

from .sql_utilities import Base


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
