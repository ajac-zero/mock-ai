FROM python:3.11-buster

WORKDIR /app

COPY . .

RUN pip install poetry
RUN poetry install

CMD ["poetry", "run", "mockai-server"]
