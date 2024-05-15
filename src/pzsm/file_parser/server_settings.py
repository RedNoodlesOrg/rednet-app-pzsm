"""server_settings.py."""

from __future__ import annotations

from .modlist import Modlist


class ServerSettings:
    """ServerSettings."""

    file_path: str
    _file_lines: list[str] | None = None
    _mods_index = -1
    _workshop_index = -1

    def __init__(self, file_path: str):
        """
        Initializes the ServerSettings object with the path to the configuration file.

        Args:
            file_path (str): Path to the configuration file.
        """
        self.file_path = file_path

    def _find_mods_indices(self) -> None:
        """
        Finds the indices for the mods and workshop items in the configuration file.

        Raises:
            ValueError: If the indices cannot be determined.
        """
        if self._file_lines is None:
            raise ValueError("Configuration data is not loaded.")

        mods_index = workshop_index = -1
        for i, line in enumerate(self._file_lines):
            if mods_index == -1 and line.strip().startswith("Mods="):
                mods_index = i
            if workshop_index == -1 and line.strip().startswith("WorkshopItems="):
                workshop_index = i
            if mods_index != -1 and workshop_index != -1:
                break
        if mods_index == -1 or workshop_index == -1:
            raise ValueError("Failed to locate mods or workshop items in the configuration file.")
        self._mods_index = mods_index
        self._workshop_index = workshop_index

    def _load(self) -> None:
        """
        Loads the configuration file into memory.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
        """
        try:
            with open(self.file_path, encoding="utf-8") as file:
                self._file_lines = file.readlines()
                self._find_mods_indices()
        except FileNotFoundError:
            raise FileNotFoundError(f"The configuration file at {self.file_path} was not found.")

    def _save(self) -> None:
        """
        Saves the modified configuration back to the file.

        Raises:
            ValueError: If there are no file lines loaded.
        """
        if self._file_lines is not None:
            with open(self.file_path, "w", encoding="utf-8") as file:
                file.writelines(self._file_lines)
        else:
            raise ValueError("Configuration data is not loaded.")

    def update_mods(self, modlist: Modlist) -> None:
        """
        Updates the mods and workshop items in the configuration file with new values from the provided modlist.

        Args:
            modlist (Modlist): The modlist containing new mods and workshop items IDs.
        """
        self._load()
        if self._file_lines is not None:
            modids, workshopids = modlist.get_ids()
            self._file_lines[self._mods_index] = f"Mods={modids}\n"
            self._file_lines[self._workshop_index] = f"WorkshopItems={workshopids}\n"
            self._save()
