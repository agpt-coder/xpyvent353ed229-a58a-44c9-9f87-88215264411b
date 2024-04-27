import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional

import prisma
import prisma.enums
import project.authenticate_user_service
import project.create_event_service
import project.create_user_service
import project.delete_event_service
import project.delete_media_service
import project.get_event_details_service
import project.get_user_profile_service
import project.list_events_service
import project.submit_feedback_service
import project.update_event_service
import project.update_profile_service
import project.upload_media_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="xpyvent",
    lifespan=lifespan,
    description="In our Python Flask MVC application, the entry point `app.py` sets up the Flask application and imports routes from `routes.py`, which maps URL paths such as `/event/display` to `event_display_controller.py` and `/event/upload` to `event_upload_controller.py`. `event_display_controller.py` retrieves event data from `event_model.py`, which utilizes `event_dao.py` for ORM-based database operations through SQLAlchemy, and renders responses using templates like `event_display_view.html` with the Jinja2 templating engine. Conversely, `event_upload_controller.py` processes data submitted through `event_form_view.html`, also managed by `event_model.py` that handles data validation and saving. `EventDTO.py` is used to pass structured data between controllers and models, ensuring a clean data flow. Frontend interactions are managed by JavaScript files such as `event_display.js` for dynamic content updates and `event_form.js` for AJAX-based form submissions. The visual styling is consistently applied through a single CSS file, `style.css`, which styles the Jinja2 templates to ensure a uniform user interface. This adaptation maintains a clear separation of concerns with a Pythonic approach to web application architecture, integrating Flask for routing and controllers, SQLAlchemy for database interaction, and Jinja2 for rendering views, all orchestrated within the versatile and dynamic environment of Python.",
)


@app.post("/user/create", response_model=project.create_user_service.CreateUserResponse)
async def api_post_create_user(
    email: str, password: str, firstName: Optional[str], lastName: Optional[str]
) -> project.create_user_service.CreateUserResponse | Response:
    """
    Endpoint for user account creation.
    """
    try:
        res = await project.create_user_service.create_user(
            email, password, firstName, lastName
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/event/create", response_model=project.create_event_service.CreateEventResponse
)
async def api_post_create_event(
    title: str, description: str, date: datetime, location: str, media: List[str]
) -> project.create_event_service.CreateEventResponse | Response:
    """
    Endpoint for creating a new event.
    """
    try:
        res = await project.create_event_service.create_event(
            title, description, date, location, media
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/profile/update",
    response_model=project.update_profile_service.UserProfileUpdateResponse,
)
async def api_put_update_profile(
    user_id: str,
    first_name: str,
    last_name: str,
    email: str,
    contact_number: Optional[str],
) -> project.update_profile_service.UserProfileUpdateResponse | Response:
    """
    Endpoint for users to update their profile information.
    """
    try:
        res = await project.update_profile_service.update_profile(
            user_id, first_name, last_name, email, contact_number
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/feedback/submit",
    response_model=project.submit_feedback_service.SubmitFeedbackResponse,
)
async def api_post_submit_feedback(
    userId: Optional[str], content: str
) -> project.submit_feedback_service.SubmitFeedbackResponse | Response:
    """
    Endpoint for users to submit feedback.
    """
    try:
        res = await project.submit_feedback_service.submit_feedback(userId, content)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/media/delete/{mediaId}",
    response_model=project.delete_media_service.DeleteMediaResponse,
)
async def api_delete_delete_media(
    mediaId: str,
) -> project.delete_media_service.DeleteMediaResponse | Response:
    """
    Endpoint for deleting media from an event.
    """
    try:
        res = await project.delete_media_service.delete_media(mediaId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/user/authenticate",
    response_model=project.authenticate_user_service.UserAuthenticationResponse,
)
async def api_post_authenticate_user(
    email: str, password: str
) -> project.authenticate_user_service.UserAuthenticationResponse | Response:
    """
    Endpoint for user login and authentication.
    """
    try:
        res = await project.authenticate_user_service.authenticate_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/event/delete/{eventId}",
    response_model=project.delete_event_service.DeleteEventResponse,
)
async def api_delete_delete_event(
    eventId: str,
) -> project.delete_event_service.DeleteEventResponse | Response:
    """
    Endpoint for deleting an event.
    """
    try:
        res = await project.delete_event_service.delete_event(eventId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/event/list", response_model=project.list_events_service.ListEventsResponse)
async def api_get_list_events() -> project.list_events_service.ListEventsResponse | Response:
    """
    Endpoint for listing all events.
    """
    try:
        res = await project.list_events_service.list_events()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/media/upload", response_model=project.upload_media_service.UploadMediaResponse
)
async def api_post_upload_media(
    eventId: str,
    media: project.upload_media_service.UploadFile,
    mediaType: prisma.enums.MediaType,
) -> project.upload_media_service.UploadMediaResponse | Response:
    """
    Endpoint for uploading media to an event.
    """
    try:
        res = await project.upload_media_service.upload_media(eventId, media, mediaType)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/event/update/{eventId}",
    response_model=project.update_event_service.UpdateEventResponse,
)
async def api_put_update_event(
    eventId: str,
    title: str,
    description: str,
    date: datetime,
    location: str,
    mediaContents: List[project.update_event_service.MediaContent],
) -> project.update_event_service.UpdateEventResponse | Response:
    """
    Endpoint for updating event details.
    """
    try:
        res = await project.update_event_service.update_event(
            eventId, title, description, date, location, mediaContents
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/event/details/{eventId}",
    response_model=project.get_event_details_service.EventDetailsResponse,
)
async def api_get_get_event_details(
    eventId: str,
) -> project.get_event_details_service.EventDetailsResponse | Response:
    """
    Endpoint for retrieving details of a specific event.
    """
    try:
        res = await project.get_event_details_service.get_event_details(eventId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/user/profile/{userId}",
    response_model=project.get_user_profile_service.UserProfileResponse,
)
async def api_get_get_user_profile(
    userId: str,
) -> project.get_user_profile_service.UserProfileResponse | Response:
    """
    Endpoint to retrieve user profile details.
    """
    try:
        res = await project.get_user_profile_service.get_user_profile(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
