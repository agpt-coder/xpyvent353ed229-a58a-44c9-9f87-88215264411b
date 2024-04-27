---
date: 2024-04-27T19:36:38.263164
author: AutoGPT <info@agpt.co>
---

# xpyvent

In our Python Flask MVC application, the entry point `app.py` sets up the Flask application and imports routes from `routes.py`, which maps URL paths such as `/event/display` to `event_display_controller.py` and `/event/upload` to `event_upload_controller.py`. `event_display_controller.py` retrieves event data from `event_model.py`, which utilizes `event_dao.py` for ORM-based database operations through SQLAlchemy, and renders responses using templates like `event_display_view.html` with the Jinja2 templating engine. Conversely, `event_upload_controller.py` processes data submitted through `event_form_view.html`, also managed by `event_model.py` that handles data validation and saving. `EventDTO.py` is used to pass structured data between controllers and models, ensuring a clean data flow. Frontend interactions are managed by JavaScript files such as `event_display.js` for dynamic content updates and `event_form.js` for AJAX-based form submissions. The visual styling is consistently applied through a single CSS file, `style.css`, which styles the Jinja2 templates to ensure a uniform user interface. This adaptation maintains a clear separation of concerns with a Pythonic approach to web application architecture, integrating Flask for routing and controllers, SQLAlchemy for database interaction, and Jinja2 for rendering views, all orchestrated within the versatile and dynamic environment of Python.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'xpyvent'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
