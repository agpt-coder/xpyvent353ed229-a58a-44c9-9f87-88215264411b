from typing import Any, Dict, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UserProfileUpdateResponse(BaseModel):
    """
    The response model returning the outcome of a user profile update attempt, including any new or unchanged data.
    """

    success: bool
    user_id: str
    message: str
    updated_fields: Dict[str, Any]


async def update_profile(
    user_id: str,
    first_name: str,
    last_name: str,
    email: str,
    contact_number: Optional[str],
) -> UserProfileUpdateResponse:
    """
    Endpoint for users to update their profile information.

    Args:
        user_id (str): The unique identifier of the user whose profile is being updated.
        first_name (str): The user's updated first name.
        last_name (str): The user's updated last name.
        email (str): The user's updated email address.
        contact_number (Optional[str]): The user's updated contact number (or None).

    Returns:
        UserProfileUpdateResponse: The response model returning the outcome of a user profile update attempt, including any new or unchanged data.

    Raises:
        ValueError: If the specified `user_id` does not exist.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
    if user is None:
        raise ValueError(f"User with id {user_id} does not exist.")
    updated_fields = {}
    profile = await prisma.models.Profile.prisma().find_unique(
        where={"userId": user_id}
    )
    if profile is not None:
        if first_name != profile.firstName:
            updated_fields["firstName"] = first_name
        if last_name != profile.lastName:
            updated_fields["lastName"] = last_name
        if contact_number:
            updated_fields["contactNumber"] = contact_number
        await prisma.models.Profile.prisma().update(
            where={"userId": user_id}, data={**updated_fields}
        )
    if email != user.email:
        existing_email = await prisma.models.User.prisma().find_unique(
            where={"email": email}
        )
        if existing_email:
            return UserProfileUpdateResponse(
                success=False,
                user_id=user_id,
                message="Email already in use, please choose a different one.",
                updated_fields={},
            )
        else:
            await prisma.models.User.prisma().update(
                where={"id": user_id}, data={"email": email}
            )
            updated_fields["email"] = email
    return UserProfileUpdateResponse(
        success=True,
        user_id=user_id,
        message="Profile updated successfully.",
        updated_fields=updated_fields,
    )
