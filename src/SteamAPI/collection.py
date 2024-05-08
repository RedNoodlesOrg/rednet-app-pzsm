"""collection.py."""

from __future__ import annotations

import json
from dataclasses import dataclass

from requests import post

from pzsm.db.mod import sync
from SteamAPI.mod import Mod
from SteamAPI.utilities import (
    get_collection_details,
    get_mods_from_details,
    get_published_file_details,
)


@dataclass
class Collection:
    """Collection."""

    mods: list[Mod]
    collection_id: int | str

    @staticmethod
    def _call_api(url: str, payload):
        """call_api."""
        response = post(url, data=payload, timeout=5)
        return json.loads(response.text)["response"]

    def __init__(self, collection_id: str):
        """Init of collection.

        Args:
            collection_id (str): Collection Id
        """
        file_ids = [
            item["publishedfileid"]
            for item in get_collection_details([collection_id])["collectiondetails"][0]["children"]
        ]
        self.mods = get_mods_from_details(get_published_file_details(file_ids))
        sync(self.mods)
