# Proposals Backend

## Local environment setup

1. Install the [GDAL](https://gdal.org/index.html) library and [Pipenv](https://pipenv.pypa.io/en/latest/) virtual environment manager on your local machine
2. Init the virtual environment: `pipenv --python 3.11`
3. Install dependencies: `pipenv install`
4. Create file `.env` using the `.env.example`
5. Migrate the database: `pipenv run python manage.py migrate`
6. Start server: `pipenv run python manage.py runserver`

## Code Style, Linter, Formatter

Use flake8 for linter: `pipenv run flake8 --statistics`

In VSC:

https://code.visualstudio.com/docs/python/linting#_enable-linters

Basic code style:

1. Use double quotes `( " )`

2. Line length not more as 99 characters

3. Imports should be grouped in the following order:

- Standard library imports.
- Related third party imports.
- Local application/library specific imports.

## Testing

To run tests: `pipenv run coverage run manage.py test apps`

## Pre-commit

- Documentation could be found [here](https://pre-commit.com/)
- To install pre-commit hook run: `pre-commit install --hook-type pre-commit`
- To check locally before the commit run: `pre-commit run --all-files`

## Celery

Worker:
`pipenv run celery -A src worker -l INFO`

Beat:
`pipenv run celery -A src beat -l INFO`

For MacOS, to avoid issues with multithreading in Python and Celery, it is required to add to the .env file following variable:
`OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`

## Docker Compose

Also for the local environment setup there's option to use docker compose, which will create db, redis and app, celery, celery-beat containers.

`docker compose up`
