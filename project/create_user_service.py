from typing import Dict, Optional

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    """
    A model that provides feedback to the client regarding the outcome of the account creation attempt. It may include successful account creation acknowledgment or error details.
    """

    success: bool
    userId: Optional[str] = None
    message: str
    errors: Optional[Dict[str, str]] = None


async def create_user(
    email: str, password: str, firstName: Optional[str], lastName: Optional[str]
) -> CreateUserResponse:
    """
    Endpoint for user account creation.

    Args:
    email (str): The email address of the user, which serves as a unique identifier and contact information.
    password (str): The password chosen by the user for account protection. This should be stored securely after being properly hashed.
    firstName (Optional[str]): The first name of the user. Optional for users who may not wish to provide it during registration.
    lastName (Optional[str]): The last name of the user. Optional as well, to accommodate privacy preferences.

    Returns:
    CreateUserResponse: A model that provides feedback to the client regarding the outcome of the account creation attempt. It may include successful account creation acknowledgment or error details.
    """
    existing_user = await prisma.models.User.prisma().find_unique(
        where={"email": email}
    )
    if existing_user:
        return CreateUserResponse(
            success=False,
            message="Email already in use",
            errors={"email": "This email is already associated with another account."},
        )
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = await prisma.models.User.prisma().create(
        data={"email": email, "password": hashed_password.decode("utf-8")}
    )
    if firstName or lastName:
        await prisma.models.Profile.prisma().create(
            data={
                "firstName": firstName or "",
                "lastName": lastName or "",
                "userId": user.id,
            }
        )
    return CreateUserResponse(
        success=True, userId=user.id, message="User created successfully"
    )
