from __future__ import annotations

from typing import Any, get_type_hints

from pydantic import BaseModel, model_validator

from .enums import Result


class PublishedFileDetailsTag(BaseModel):
    tag: str


def get_optional_fields(cls) -> set:
    """Returns a set of all fields that are declared as Optional.

    Returns:
        set: Unique list of all optional fields
    """
    optional_fields = set()
    type_hints = get_type_hints(cls, include_extras=True)
    for field_name, field_type in type_hints.items():
        if type(None) in getattr(field_type, "__args__", ()):
            optional_fields.add(field_name)
    return optional_fields


class PublishedFileDetails(BaseModel):

    publishedfileid: str
    result: Result
    creator: str | None = "NOT FOUND"
    creator_app_id: int | None = None
    consumer_app_id: int | None = None
    filename: str | None = "NOT FOUND"
    file_size: str | None = "NOT FOUND"
    file_url: str | None = "NOT FOUND"
    hcontent_file: str | None = "NOT FOUND"
    preview_url: str | None = "NOT FOUND"
    hcontent_preview: str | None = "NOT FOUND"
    title: str | None = "NOT FOUND"
    description: str | None = "NOT FOUND"
    time_created: int | None = None
    time_updated: int | None = None
    visibility: int | None = None
    banned: int | None = None
    ban_reason: str | None = "NOT FOUND"
    subscriptions: int | None = None
    favorited: int | None = None
    lifetime_subscriptions: int | None = None
    lifetime_favorited: int | None = None
    views: int | None = None
    tags: list[PublishedFileDetailsTag] | None = None

    @model_validator(mode="before")
    @classmethod
    def check_card_number_omitted(cls, data: Any) -> Any:
        required_fields = get_optional_fields(PublishedFileDetails)
        if isinstance(data, dict) and "result" in data:
            if Result(data["result"]) is Result.OK:
                for field in required_fields:
                    assert field in data and data[field] is not None, f"{field} is required when result is {Result.OK}"
        return data
