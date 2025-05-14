FROM python:3.10
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

WORKDIR /code/app

## TODO: if there would be a database, should add "alembic upgrade head" before run server
CMD bash -c "uvicorn main:main --host 0.0.0.0 --port 8080"