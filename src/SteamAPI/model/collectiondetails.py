from __future__ import annotations

from typing import List

from pydantic import BaseModel

from SteamAPI.model.publishedfile import PublishedFile


class CollectionDetails(BaseModel):
    publishedfileid: str
    result: int
    children: list[PublishedFile]


class CollectionDetailsResponse(BaseModel):
    result: int
    resultcount: int
    collectiondetails: list[CollectionDetails]
