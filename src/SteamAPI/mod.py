"""mod.py."""

from __future__ import annotations

import re
from dataclasses import dataclass

from SteamAPI.model import PublishedFileDetails


@dataclass
class ModId:
    """ModId."""

    id: str
    enabled: bool

    def __init__(self, mod_id: str, enabled: bool = False):
        """Init of ModId.

        Args:
            mod_id (str): Mod id
            enabled (bool, optional): Enable flag. Defaults to False.
        """
        self.id = mod_id
        self.enabled = enabled


def extract_id(text) -> list[ModId]:
    """extract_id."""
    matches = re.findall(r"Mod\s?ID:\s*(?:\[\/b\] )?(.*?)(?:\r|\[\/hr\]|$|\n)", text, re.IGNORECASE)
    unique_matches = {match.strip() for match in matches if match}
    matches_with_flag = [ModId(match, len(unique_matches) == 1) for match in unique_matches]
    matches_with_flag = sorted(matches_with_flag, key=lambda mod_id: len(mod_id.id))
    return matches_with_flag


@dataclass
class Mod:
    """Mod."""

    workshop_id: str
    description: str
    mod_ids: list[ModId]
    thumbnail: str
    name: str

    def __init__(self, workshop_details: PublishedFileDetails):
        """__init__."""

        self.description = workshop_details.description if workshop_details.description is not None else "NOT FOUND"
        self.mod_ids = extract_id(self.description)
        self.workshop_id = workshop_details.publishedfileid
        self.thumbnail = workshop_details.preview_url if workshop_details.preview_url is not None else "NOT FOUND"
        self.name = workshop_details.title if workshop_details.title is not None else "NOT FOUND"
        self.status = workshop_details.result
