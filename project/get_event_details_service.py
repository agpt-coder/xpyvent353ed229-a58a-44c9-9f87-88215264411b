from datetime import datetime
from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class Media(BaseModel):
    """
    Describes the media content related to an event, including type and URL.
    """

    type: prisma.enums.MediaType
    url: str


class EventDetailsResponse(BaseModel):
    """
    A comprehensive model that describes the detailed information of an event, including metadata and associated media.
    """

    id: str
    title: str
    description: str
    date: datetime
    location: str
    media: List[Media]


async def get_event_details(eventId: str) -> EventDetailsResponse:
    """
    Endpoint for retrieving details of a specific event.

    Args:
        eventId (str): The unique identifier of the event whose details are to be retrieved.

    Returns:
        EventDetailsResponse: A comprehensive model that describes the detailed information of an event, including metadata and associated media.
    """
    event = await prisma.models.Event.prisma().find_unique(
        where={"id": eventId}, include={"Media": True}
    )
    if not event:
        raise ValueError(f"Event with id {eventId} not found.")
    media_list = [Media(type=media.type.name, url=media.url) for media in event.Media]
    return EventDetailsResponse(
        id=event.id,
        title=event.title,
        description=event.description,
        date=event.date,
        location=event.location,
        media=media_list,
    )
