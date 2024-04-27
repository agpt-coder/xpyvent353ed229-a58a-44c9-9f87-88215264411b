from datetime import datetime
from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class MediaContent(BaseModel):
    """
    Media content such as images or videos linked to the event.
    """

    mediaId: str
    type: prisma.enums.MediaType
    url: str


class UpdateEventResponse(BaseModel):
    """
    Response model for the event update operation, indicating success and returning the updated event details.
    """

    success: bool
    eventId: str
    updatedFields: List[str]


async def update_event(
    eventId: str,
    title: str,
    description: str,
    date: datetime,
    location: str,
    mediaContents: List[MediaContent],
) -> UpdateEventResponse:
    """
    Endpoint for updating event details.

    Args:
        eventId (str): The unique identifier of the event to be updated.
        title (str): The new title for the event.
        description (str): The new description of the event.
        date (datetime): The updated date and time of the event.
        location (str): The updated location of the event.
        mediaContents (List[MediaContent]): List of media content associated with the event.

    Returns:
        UpdateEventResponse: Response model for the event update operation, indicating success and returning the updated event details.
    """
    updatedFields = []
    event = await prisma.models.Event.prisma().find_unique(where={"id": eventId})
    if not event:
        return UpdateEventResponse(success=False, eventId=eventId, updatedFields=[])
    await prisma.models.Event.prisma().update(
        where={"id": eventId},
        data={
            "title": title,
            "description": description,
            "date": date,
            "location": location,
        },
    )
    updatedFields.extend(["title", "description", "date", "location"])
    if mediaContents:
        await prisma.models.Media.prisma().delete_many(where={"eventId": eventId})
        for media_content in mediaContents:
            await prisma.models.Media.prisma().create(
                data={
                    "type": media_content.type,
                    "url": media_content.url,
                    "eventId": eventId,
                }
            )
        updatedFields.append("mediaContents")
    return UpdateEventResponse(
        success=True, eventId=eventId, updatedFields=updatedFields
    )
