from __future__ import annotations

import pytest
import requests_mock

from SteamAPI import Collection
from SteamAPI.collection import GETCOLLECTIONDETAILS, GETPUBLISHEDFILEDETAILS

modids = [
    "shelter-4912",
    "shelter-4912clean",
    "shelter-2228",
    "shelter-2533",
    "shelter-2533clean",
    "shelter-2926",
    "shelter-2926clean",
    "shelter-4030",
    "shelter-4515",
    "shelter-4515clean",
    "tower-1326",
    "tower-4722",
    "shelters-tileset",
]


@pytest.mark.unit
def test_collection(fixture_steamapi):
    input_published_file_details_response, input_collection_details_response = fixture_steamapi
    with requests_mock.Mocker(real_http=False) as m:
        m.post(GETCOLLECTIONDETAILS, json=input_collection_details_response)
        m.post(GETPUBLISHEDFILEDETAILS, json=input_published_file_details_response)

        collection = Collection("3221219310")
        assert collection.collection_id == "1234567890"
        for mod in collection.mods:
            for id in mod.mod_ids:
                assert id.id in modids
        assert len(collection.mods) == 9

    pass
