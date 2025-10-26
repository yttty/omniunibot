FROM python:3.12-slim-bookworm

RUN mkdir /src
ADD ./omniunibot /src/omniunibot
COPY ./pyproject.toml /src
COPY ./README.md /src

RUN pip install --no-cache-dir /src && rm -r /src

WORKDIR /app
ENTRYPOINT ["gunicorn", "omniunibot.api:app", "--bind", "0.0.0.0:9999", "--worker-class", "aiohttp.GunicornWebWorker"]
