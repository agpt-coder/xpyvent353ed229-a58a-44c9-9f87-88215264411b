from typing import Optional

import prisma
import prisma.models
from passlib.context import CryptContext
from pydantic import BaseModel


class UserAuthenticationResponse(BaseModel):
    """
    Model for returning the result of the authentication attempt. This will typically include a token for successful authentication or an error message for failures.
    """

    token: Optional[str] = None
    message: str
    success: bool


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(email: str, password: str) -> UserAuthenticationResponse:
    """
    Endpoint for user login and authentication.

    First, it attempts to retrieve the user from the database using the given email.
    If the user is found, it then verifies the password using bcrypt.
    On successful verification, it generates a token (for simplicity, it will return a dummy token here).
    On failure, it returns an appropriate message.

    Args:
    email (str): The user's email address as the identifier for the login attempt.
    password (str): The user's password, which will be compared against a hashed version stored within the system.

    Returns:
    UserAuthenticationResponse: Model for returning the result of the authentication attempt. This will typically include a token for successful authentication or an error message for failures.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if user and pwd_context.verify(password, user.password):
        token = "dummy_token"
        return UserAuthenticationResponse(
            token=token, message="Authentication successful.", success=True
        )
    else:
        return UserAuthenticationResponse(
            message="Authentication failed. Incorrect email or password.", success=False
        )
