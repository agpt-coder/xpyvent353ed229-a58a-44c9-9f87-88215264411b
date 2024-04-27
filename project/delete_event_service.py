import prisma
import prisma.models
from pydantic import BaseModel


class DeleteEventResponse(BaseModel):
    """
    This model communicates the result of a delete event attempt, indicating success or failure with an appropriate message.
    """

    success: bool
    message: str


async def delete_event(eventId: str) -> DeleteEventResponse:
    """
    Endpoint for deleting an event.

    Args:
        eventId (str): The unique identifier for the event to be deleted.

    Returns:
        DeleteEventResponse: This model communicates the result of a delete event attempt, indicating success or failure with an appropriate message.
    """
    event = await prisma.models.Event.prisma().delete(where={"id": eventId})
    if event:
        return DeleteEventResponse(
            success=True, message="prisma.models.Event successfully deleted."
        )
    else:
        return DeleteEventResponse(
            success=False, message="Failed to delete the event. It may not exist."
        )
