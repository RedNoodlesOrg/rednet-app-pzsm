"""collection.py."""

from __future__ import annotations

from dataclasses import dataclass

from flask import json
from requests import post

from SteamAPI.mod import Mod
from SteamAPI.model import (CollectionDetails, CollectionDetailsResponse,
                            PublishedFileDetails, PublishedFileDetailsResponse,
                            Result, WorkshopFileType)

BASEURL = "https://api.steampowered.com/ISteamRemoteStorage"
GETCOLLECTIONDETAILS = BASEURL + "/GetCollectionDetails/v1/"
GETPUBLISHEDFILEDETAILS = BASEURL + "/GetPublishedFileDetails/v1/"


def _list_to_kv(lst) -> dict:
    return {f"publishedfileids[{i}]": v for i, v in enumerate(lst)}


def _call_api(url: str, count_type: str, ids: list[str]) -> dict:
    payload = {count_type: len(ids), **_list_to_kv(ids)}
    response = post(url, data=payload, timeout=5)
    return json.loads(response.text)["response"]


@dataclass
class Collection:
    mods: list[Mod]
    collection_id: int | str

    def __init__(self, collection_id: str):
        """Init of collection.

        Args:
            collection_id (str): Collection Id
        """
        collection_details = self._get_collection_details([collection_id])
        self.collection_id = collection_details.publishedfileid
        pub_file_details = self._get_published_file_details(collection_details)
        self.mods = self._get_mods_from_details(pub_file_details)

    @staticmethod
    def _get_collection_details(ids: list[str]) -> CollectionDetails:
        response = CollectionDetailsResponse.model_validate(_call_api(GETCOLLECTIONDETAILS, "collectioncount", ids))

        if response.result is not Result.OK or response.resultcount != 1:
            raise ValueError("API Response is not as expected")
        return response.collectiondetails[0]

    @staticmethod
    def _get_published_file_details(details: CollectionDetails) -> list[PublishedFileDetails]:
        ids = Collection._get_mod_ids(details)

        response = PublishedFileDetailsResponse.model_validate(_call_api(GETPUBLISHEDFILEDETAILS, "itemcount", ids))

        return response.publishedfiledetails

    @staticmethod
    def _get_mod_ids(details: CollectionDetails) -> list[str]:
        ids = []
        for file in details.children:
            if file.filetype is WorkshopFileType.COLLECTION:
                collection_details = Collection._get_collection_details([file.publishedfileid])
                ids.extend(Collection._get_mod_ids(collection_details))
            elif file.filetype is WorkshopFileType.COMMUNITY:
                ids.append(file.publishedfileid)
        return ids

    @staticmethod
    def _get_mods_from_details(files: list[PublishedFileDetails]) -> list[Mod]:
        mods = []
        for file in files:
            mods.append(Mod(file))
        return mods
