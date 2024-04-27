import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UploadFile(BaseModel):
    """
    Represents the file upload object, capturing both the content and metadata of the file.
    """

    filename: str
    content: bytes
    content_type: str


class UploadMediaResponse(BaseModel):
    """
    Response payload confirming the successful media upload.
    """

    mediaId: str
    message: str


async def upload_media(
    eventId: str, media: UploadFile, mediaType: prisma.enums.MediaType
) -> UploadMediaResponse:
    """
    Endpoint for uploading media to an event.

    Args:
        eventId (str): Identifier for the event to which the media belongs.
        media (UploadFile): The multimedia file to be uploaded.
        mediaType (prisma.enums.MediaType): The type of media being uploaded (e.g., image, video).

    Returns:
        UploadMediaResponse: Response payload confirming the successful media upload.
    """
    media_url = f"https://yourmediastorage.url/{media.filename}"
    created_media = await prisma.models.Media.prisma().create(
        data={"type": mediaType, "url": media_url, "eventId": eventId}
    )
    return UploadMediaResponse(
        mediaId=created_media.id, message="prisma.models.Media uploaded successfully."
    )
