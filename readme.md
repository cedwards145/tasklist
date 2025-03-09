# Task List App
A Task List built using FastAPI and SQLite

## How To Run
Using pip, install all requirements from `requirements.txt`
`pip install -r requirements.txt`

From the root folder of this repository, run the app using the following command:
`fastapi run ./tasklist/main.py`

The API will be available on http://localhost:8000, and the Swagger documentation is available at http://localhost:8000/docs

## How To Develop
Using pip, additionally install all requirements from `requirements_dev.txt`
`pip install -r requirements_dev.txt`

This includes tools not required for the program to run, but useful for development. These include:
- [black](https://github.com/psf/black), a python formatter that has been used for this project
- [pytest](https://docs.pytest.org/en/stable/), a testing framework used on this project

To run black and format the entire project, run the following command from the root of the repository:
`black .`
Please note, this command will alter the contents of files directly. Ensure work is committed or otherwise backed up before running this command.

Unit tests are located under the tests directory. Run the following command from the root of the repository to run all unit tests:
`pytest`

## Areas to Improve
- FastAPI @app.on_event("startup") annotation has been deprecated. Currently working, but should be replaced with [Lifespan Events](https://fastapi.tiangolo.com/advanced/events/#lifespan)
- Better handling of validation errors. Currently App returns 500 internal error when data that does not conform to a model is supplied. This should be caught and more descriptive 400 Bad Request should be returned instead.
- Priorities requiring values between 1 and 3 is documented, but separately and repeatedly. This is difficult to change and error-prone. Priority could be handled in a more type-safe way as an Enum.