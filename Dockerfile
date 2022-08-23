FROM python:latest

COPY . /src/app/

WORKDIR /src/app/

RUN apt-get update && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

CMD poetry run python app/__init__.py
