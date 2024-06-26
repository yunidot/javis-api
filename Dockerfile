FROM python:3.11-slim as requirement-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-slim

WORKDIR /javis

COPY --from=requirement-stage /tmp/requirements.txt /javis/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /javis/requirements.txt

COPY ./ .

RUN ENV=prod

CMD ["gunicorn", "--bind", "0:12800", "app.main:app", "--worker-class", "uvicorn.workers.UvicornWorker"]
