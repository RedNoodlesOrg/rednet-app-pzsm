"""utilities.py."""

from __future__ import annotations

from flask import json
from requests import post

from SteamAPI.mod import Mod
from SteamAPI.model.collectiondetails import (CollectionDetails,
                                              CollectionDetailsResponse)
from SteamAPI.model.publishedfiledetails import (PublishedFileDetails,
                                                 PublishedFileDetailsResponse)
from SteamAPI.model.workshopfiletype import WorkshopFileType

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


def get_collection_details(ids: list[str]) -> CollectionDetails:
    """get_collection_details."""

    response = CollectionDetailsResponse.model_validate(
        _call_api(GETCOLLECTIONDETAILS, {"collectioncount": len(ids), **list_to_kv(ids)})
    )

    if response.result != 1 or response.resultcount != 1:
        raise ValueError("API Response is not as expected")
    return response.collectiondetails[0]


def get_mod_ids(details: CollectionDetails) -> list[str]:
    ids = []
    for file in details.children:
        if file.filetype is WorkshopFileType.COLLECTION:
            collection_details = get_collection_details([file.publishedfileid])
            ids.extend(get_mod_ids(collection_details))
        elif file.filetype is WorkshopFileType.COMMUNITY:
            ids.append(file.publishedfileid)
    return ids


def get_published_file_details(details: CollectionDetails) -> list[PublishedFileDetails]:
    """get_published_file_details."""
    ids = get_mod_ids(details)
    response = PublishedFileDetailsResponse.model_validate(
        _call_api(GETPUBLISHEDFILEDETAILS, {"itemcount": len(ids), **list_to_kv(ids)})
    )
    return response.publishedfiledetails


def get_mods_from_details(files: list[PublishedFileDetails]):
    """get_mods_from_details."""
    mods = []
    for file in files:
        mods.append(Mod(file.model_dump()))
    return mods
