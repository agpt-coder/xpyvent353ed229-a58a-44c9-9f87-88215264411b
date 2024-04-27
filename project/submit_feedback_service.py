from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class SubmitFeedbackResponse(BaseModel):
    """
    Confirms the successful submission of feedback, including the ID of the newly created feedback entry.
    """

    success: bool
    feedbackId: str
    message: str


async def submit_feedback(
    userId: Optional[str], content: str
) -> SubmitFeedbackResponse:
    """
    Endpoint for users to submit feedback.

    Args:
        userId (Optional[str]): Optional userId to identify the user submitting feedback.
        content (str): The content of the feedback provided by the user.

    Returns:
        SubmitFeedbackResponse: Confirms the successful submission of feedback, including the ID of the newly created feedback entry.
    """
    try:
        feedback_entry = await prisma.models.Feedback.prisma().create(
            data={"content": content, "userId": userId if userId else None}
        )
        return SubmitFeedbackResponse(
            success=True,
            feedbackId=feedback_entry.id,
            message="Your feedback has been submitted successfully.",
        )
    except Exception as e:
        return SubmitFeedbackResponse(
            success=False, feedbackId="", message=f"Failed to submit feedback: {str(e)}"
        )
