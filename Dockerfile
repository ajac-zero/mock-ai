FROM python:3.11-buster

WORKDIR /app

RUN pip install poetry

COPY . .

RUN poetry install

CMD ["poetry", "run", "python", "-m", "scripts.docker_start"]
