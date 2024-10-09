FROM python:3.10.15-slim

RUN apt-get update && apt-get -y install \
    build-essential \
    libpq-dev \
    python3-dev \
    && apt-get clean

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv && \
    pipenv install --system --deploy

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
