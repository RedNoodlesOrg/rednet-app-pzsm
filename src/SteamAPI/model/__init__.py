# flake8: noqa: F401
from __future__ import annotations

from pydantic import BaseModel

from .enums import Result, WorkshopFileType
from .publishedfiledetails import PublishedFileDetails


class PublishedFile(BaseModel):
    sortorder: int
    publishedfileid: str
    filetype: WorkshopFileType


class CollectionDetails(BaseModel):
    result: Result
    publishedfileid: str
    children: list[PublishedFile]


class PublishedFileDetailsResponse(BaseModel):
    result: Result
    resultcount: int
    publishedfiledetails: list[PublishedFileDetails]


class CollectionDetailsResponse(BaseModel):
    result: Result
    resultcount: int
    collectiondetails: list[CollectionDetails]
