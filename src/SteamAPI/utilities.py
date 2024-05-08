"""utilities.py."""

from __future__ import annotations

from flask import json
from requests import post

from SteamAPI.mod import Mod

BASEURL = "https://api.steampowered.com/ISteamRemoteStorage"
GETCOLLECTIONDETAILS = BASEURL + "/GetCollectionDetails/v1/"
GETPUBLISHEDFILEDETAILS = BASEURL + "/GetPublishedFileDetails/v1/"


def list_to_kv(lst) -> dict:
    """list_to_kv."""
    return {f"publishedfileids[{i}]": v for i, v in enumerate(lst)}


def _call_api(url: str, payload) -> dict:
    """_call_api."""
    response = post(url, data=payload, timeout=5)
    return json.loads(response.text)["response"]


def get_collection_details(ids: list[str]) -> dict:
    """get_collection_details."""
    return _call_api(GETCOLLECTIONDETAILS, {"collectioncount": len(ids), **list_to_kv(ids)})


def get_published_file_details(ids: list[str]) -> dict:
    """get_published_file_details."""
    return _call_api(GETPUBLISHEDFILEDETAILS, {"itemcount": len(ids), **list_to_kv(ids)})


def get_mods_from_details(details: dict):
    """get_mods_from_details."""
    mods = []
    for file in details["publishedfiledetails"]:
        creator_app_id = file.get("creator_app_id")
        if creator_app_id and creator_app_id == 766:
            file_ids = [
                item["publishedfileid"]
                for item in get_collection_details([file["publishedfileid"]])["collectiondetails"][0]["children"]
            ]
            mods.extend(get_mods_from_details(get_published_file_details(file_ids)))
        else:
            mods.append(Mod(file))
    return mods
