from __future__ import annotations

from enum import Enum


class WorkshopFileType(Enum):
    """Defines the types of files that can be associated with workshop items within the platform. These types
    help in categorizing the workshop items for better management and accessibility.

    Attributes:
        COMMUNITY (int): Normal Workshop item that can be subscribed to.
        MICROTRANSACTION (int): Workshop item intended for voting for potential sale in-game. See Curated Workshop.
        COLLECTION (int): A collection of Workshop items.
        ART (int): Artwork.
        VIDEO (int): External video.
        SCREENSHOT (int): Screenshot.
        WEBGUIDE (int): Steam web guide.
        INTEGRATEDGUIDE (int): Guide integrated within an application.
        MERCH (int): Workshop merchandise intended for voting for potential sale.
        CONTROLLERBINDING (int): Steam Controller bindings.
        STEAMVIDEO (int): Steam video content.
    """

    COMMUNITY = 0
    MICROTRANSACTION = 1
    COLLECTION = 2
    ART = 3
    VIDEO = 4
    SCREENSHOT = 5
    WEBGUIDE = 9
    INTEGRATEDGUIDE = 10
    MERCH = 11
    CONTROLLERBINDING = 12
    STEAMVIDEO = 14
