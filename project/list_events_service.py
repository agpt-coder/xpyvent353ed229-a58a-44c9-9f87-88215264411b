from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class MediaDetails(BaseModel):
    """
    Details about the multimedia content associated with an event.
    """

    url: str
    type: str


class EventDetails(BaseModel):
    """
    Details about an individual event, optimized for listing purposes.
    """

    id: str
    title: str
    description: str
    date: datetime
    location: str
    media: List[MediaDetails]


class ListEventsResponse(BaseModel):
    """
    The response model providing a list of events, including their basic information and associated multimedia content. The aim is to provide enough detail to allow users to identify events of interest without overwhelming the response body with too much intricate detail.
    """

    events: List[EventDetails]


async def list_events() -> ListEventsResponse:
    """
    Endpoint for listing all events.

    Returns:
    ListEventsResponse: The response model providing a list of events, including their basic information and associated multimedia content. The aim is to provide enough detail to allow users to identify events of interest without overwhelming the response body with too much intricate detail.
    """
    events = await prisma.models.Event.prisma().find_many(include={"Media": True})
    event_details_list = []
    for event in events:
        media_details = [
            MediaDetails(url=media.url, type=media.type.name) for media in event.Media
        ]
        event_details = EventDetails(
            id=event.id,
            title=event.title,
            description=event.description,
            date=event.date,
            location=event.location,
            media=media_details,
        )
        event_details_list.append(event_details)
    list_events_response = ListEventsResponse(events=event_details_list)
    return list_events_response
