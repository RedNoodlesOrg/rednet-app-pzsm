"""collection.py."""

from __future__ import annotations

from dataclasses import dataclass

from SteamAPI.mod import Mod
from SteamAPI.utilities import (get_collection_details, get_mods_from_details,
                                get_published_file_details)


@dataclass
class Collection:
    """Collection."""

    mods: list[Mod]
    collection_id: int | str

    def __init__(self, collection_id: str):
        """Init of collection.

        Args:
            collection_id (str): Collection Id
        """
        collection_details = get_collection_details([collection_id])
        pub_file_details = get_published_file_details(collection_details)
        self.mods = get_mods_from_details(pub_file_details)
