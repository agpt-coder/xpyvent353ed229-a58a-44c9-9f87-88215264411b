from enum import Enum

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UserProfileResponse(BaseModel):
    """
    Model representing detailed user profile information, containing both personal data and account specifics.
    """

    userId: str
    firstName: str
    lastName: str
    email: str
    role: prisma.enums.Role
    createdAt: str
    updatedAt: str


class Role(Enum):
    ATTENDEE: str = "ATTENDEE"
    ADMIN: str = "ADMIN"
    GUEST: str = "GUEST"


async def get_user_profile(userId: str) -> UserProfileResponse:
    """
    Endpoint to retrieve user profile details using a Prisma Client.

    Args:
        userId (str): Unique identifier of the user whose profile information is being requested.

    Returns:
        UserProfileResponse: Model representing detailed user profile information, containing both personal data and account specifics.
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"id": userId}, include={"Profile": True}
    )
    if not user or not user.Profile:
        raise Exception("User or User Profile not found")
    user_profile_response = UserProfileResponse(
        userId=user.id,
        firstName=user.Profile.firstName,
        lastName=user.Profile.lastName,
        email=user.email,
        role=user.role,
        createdAt=user.createdAt.isoformat(),
        updatedAt=user.updatedAt.isoformat(),
    )
    return user_profile_response
