import prisma
import prisma.models
from pydantic import BaseModel


class DeleteMediaResponse(BaseModel):
    """
    Response model for acknowledging the deletion of media. Includes status of the operation and any specific messages.
    """

    success: bool
    message: str


async def delete_media(mediaId: str) -> DeleteMediaResponse:
    """
    Endpoint for deleting media from an event.

    Args:
    mediaId (str): Unique identifier for the media to be deleted.

    Returns:
    DeleteMediaResponse: Response model for acknowledging the deletion of media. Includes status of the operation and any specific messages.

    Example:
        mediaId = 'cuid123'
        response = await delete_media(mediaId)
        > DeleteMediaResponse(success=True, message='Media deleted successfully.')
    """
    try:
        media = await prisma.models.Media.prisma().find_unique(where={"id": mediaId})
        if media:
            await prisma.models.Media.prisma().delete(where={"id": mediaId})
            return DeleteMediaResponse(
                success=True, message="Media deleted successfully."
            )
        else:
            return DeleteMediaResponse(success=False, message="Media not found.")
    except Exception as e:
        return DeleteMediaResponse(
            success=False, message=f"An error occurred: {str(e)}"
        )
