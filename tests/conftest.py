from __future__ import annotations

import json

import pytest


@pytest.fixture
def input_collection_details_response() -> dict:
    """
    This fixture is used to simulate the response from the 'GETCOLLECTIONDETAILS' endpoint
    during testing by providing a predefined JSON response.

    Returns:
        dict: A dictionary representing the JSON response from the 'GETCOLLECTIONDETAILS' endpoint.
    """
    with open("tests/fixtures/CollectionDetailsResponse.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def input_published_file_details_response() -> dict:
    """
    This fixture is used to simulate the response from the 'GETPUBLISHEDFILEDETAILS' endpoint
    during testing by providing a predefined JSON response.

    Returns:
        dict: A dictionary representing the JSON response from the 'GETPUBLISHEDFILEDETAILS' endpoint.
    """
    with open("tests/fixtures/PublishedFileDetailsResponse.json", encoding="utf-8") as f:
        return json.load(f)
