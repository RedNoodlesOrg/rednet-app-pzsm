"""mod.py."""

from __future__ import annotations

import re
from dataclasses import dataclass


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

    def __init__(self, workshop_details: dict):
        """__init__."""
        self.description = workshop_details.get("description", "NOT FOUND")
        self.mod_ids = extract_id(workshop_details.get("description", ""))
        self.workshop_id = workshop_details.get("publishedfileid", "NOT FOUND")
        self.thumbnail = workshop_details.get("preview_url", "NOT FOUND")
        self.name = workshop_details.get("title", "NOT FOUND")
