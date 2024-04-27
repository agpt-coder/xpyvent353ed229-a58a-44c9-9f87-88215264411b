from datetime import datetime
from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CreateEventResponse(BaseModel):
    """
    The output model providing feedback after attempting to create a new event.
    """

    success: bool
    event_id: Optional[str] = None
    message: Optional[str] = None


async def create_event(
    title: str, description: str, date: datetime, location: str, media: List[str]
) -> CreateEventResponse:
    """
    Endpoint for creating a new event.

    Args:
    title (str): The title or name of the event.
    description (str): A detailed description of the event.
    date (datetime): The scheduled date and time of the event. Should follow ISO 8601 format.
    location (str): The location where the event is held.
    media (List[str]): A list of identifiers for multimedia content associated with the event. This can be images or videos.

    Returns:
    CreateEventResponse: The output model providing feedback after attempting to create a new event.
    """
    try:
        user_id = "placeholder_user_id"
        event = await prisma.models.Event.prisma().create(
            data={
                "title": title,
                "description": description,
                "date": date,
                "location": location,
                "createdBy": user_id,
                "Media": {"create": [{"url": url, "type": "IMAGE"} for url in media]},
            }
        )
        return CreateEventResponse(
            success=True, event_id=event.id, message="Event created successfully."
        )
    except Exception as e:
        return CreateEventResponse(
            success=False, message="Failed to create event due to an internal error."
        )
