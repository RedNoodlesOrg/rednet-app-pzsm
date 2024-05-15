"""modlist.py."""

from __future__ import annotations

from SteamAPI.mod import Mod


class Modlist:
    """
    Represents a list of game mods with functionalities to manage and retrieve mod and workshop IDs.

    Attributes:
        mods ( list[Mod] | None): List of mod objects.
        modids (str | None): Concatenated string of mod IDs.
        workshopids (str | None): Concatenated string of workshop IDs.
    """

    mods: list[Mod] | None
    modids: str | None
    workshopids: str | None

    def __init__(self, mods: list[Mod] | None = None, modids: str | None = None, workshopids: str | None = None):
        """Initialize the Modlist.

        Args:
            mods (list[Mod] | None, optional): List of mods. Defaults to None.
            modids (str | None, optional): List of mod IDs. Defaults to None.
            workshopids (str | None, optional): List of workshop IDs. Defaults to None.

        Raises:
            ValueError: Occurs when either both mods and IDs are None or both are set.
        """
        if mods is None:
            if modids is None or workshopids is None:
                raise ValueError("Cannot leave out mods and IDs!")
        else:
            if modids is not None or workshopids is not None:
                raise ValueError("Cannot set mods and IDs!")
        self.mods = mods
        self.modids = modids
        self.workshopids = workshopids

    def get_ids(self) -> tuple[str, str]:
        """Get the mod IDs and workshop IDs.

        Returns:
            A tuple containing the mod IDs and workshop IDs as strings.

        Raises:
            ValueError: If the mods are not set.
        """
        if self.modids is None or self.workshopids is None:
            if self.mods:
                mod_ids = []
                for mod in self.mods:
                    for mod_id in mod.mod_ids:
                        if mod_id.enabled:
                            mod_ids.append(mod_id.id)
                self.modids = ";".join(mod_ids)
                self.workshopids = ";".join([mod.workshop_id for mod in self.mods])
            else:
                raise ValueError("Mods not set!")
        return self.modids, self.workshopids
