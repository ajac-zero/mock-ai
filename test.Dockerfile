FROM python:3.13-slim

RUN apt-get update && apt-get install -y gcc

# Install dependencies
RUN pip install poetry

# Set up working directory
WORKDIR /app

# Copy everything to the working directory
COPY . /app

# Install the dependencies
RUN poetry install --extras "all"


# Expose the port
EXPOSE 8100

# Set the entrypoint
ENTRYPOINT ["poetry", "run", "ai-mock", "server", "-h", "0.0.0.0", "-p", "8100"]