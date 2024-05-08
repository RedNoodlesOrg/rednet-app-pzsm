"""server_settings.py."""

from __future__ import annotations

from .modlist import Modlist


def find_mods_indices(lines: list[str]):
    """find_mods_indices."""
    mods_index = -1
    workshop_index = -1
    for i, line in enumerate(lines):
        if mods_index == -1 and line.startswith("Mods="):
            mods_index = i
        elif workshop_index == -1 and line.startswith("WorkshopItems="):
            workshop_index = i
        if mods_index != -1 and workshop_index != -1:
            break
    return mods_index, workshop_index


class ServerSettings:
    """ServerSettings."""

    file_path: str
    _file_lines: list[str] | None = None
    _mods_index = -1
    _workshop_index = -1

    def __init__(self, file_path: str):
        """Init of ServerSettings.

        Args:
            file_path (str): Path to configuration file
        """
        self.file_path = file_path

    def load(self):
        """load."""
        with open(self.file_path, encoding="utf-8") as configfile:
            self._file_lines = configfile.readlines()
            self._mods_index, self._workshop_index = find_mods_indices(self._file_lines)
            if self._mods_index == -1 or self._workshop_index == -1:
                raise ValueError("Could not determine line number for replacing the mods.")

    def save(self):
        """save."""
        if self._file_lines:
            with open(self.file_path, "w", encoding="utf-8") as configfile:
                configfile.writelines(self._file_lines)
        else:
            raise ValueError("Config never loaded")

    def update_mods(self, modlist: Modlist):
        """update_mods."""
        if self._file_lines is None:
            self.load()
        if self._file_lines:
            modids, workshopids = modlist.get_ids()
            self._file_lines[self._mods_index] = "Mods=" + modids + "\n"
            self._file_lines[self._workshop_index] = "WorkshopItems=" + workshopids + "\n"
        else:
            raise ValueError("Was not able to read config file")
        return self
