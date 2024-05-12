from __future__ import annotations

import json
import os
import sqlite3

import pytest

from pzsm.db.sql_utilities import EngineSingleton


@pytest.fixture
def fixture_steamapi():
    """
    This fixture is used to simulate the response from the 'GETCOLLECTIONDETAILS' and 'GETPUBLISHEDFILEDETAILS'
    endpoints during testing by providing predefined JSON responses.

    yield:
        dict: A dictionary representing the JSON response from the 'GETPUBLISHEDFILEDETAILS' endpoint.
        dict: A dictionary representing the JSON response from the 'GETCOLLECTIONDETAILS' endpoint.
    """

    with open("tests/data/PublishedFileDetailsResponse.json", encoding="utf-8") as f:
        input_published_file_details_response = json.load(f)
    with open("tests/data/CollectionDetailsResponse.json", encoding="utf-8") as f:
        input_collection_details_response = json.load(f)

    yield input_published_file_details_response, input_collection_details_response


@pytest.fixture
def fixture_db():
    """
    Fixture function that sets up a database connection and provides input_mod_json and con objects.

    yield:
        dict: A dictionary representing a mod object.
        sqlite3.Connection: A connection object to the SQLite database.
    """
    with open("tests/data/PublishedFileDetails.json", encoding="utf-8") as f:
        input_mod_json = json.load(f)

    con = sqlite3.connect("mods.db")
    yield input_mod_json, con

    con.close()
    EngineSingleton.get_instance().dispose()
    os.remove("mods.db")
