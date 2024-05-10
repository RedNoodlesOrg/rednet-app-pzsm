from __future__ import annotations

from pydantic import BaseModel

from SteamAPI.model.workshopfiletype import WorkshopFileType


class PublishedFile(BaseModel):
    publishedfileid: str
    sortorder: int
    filetype: WorkshopFileType
