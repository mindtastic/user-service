# user-service
The user service for the mindtastic backend

## Requirements

Python >= 3.9

## Setup
    pip install -r requirements.txt

Get MongoDB credentials and add them to .env file.

    cp .env.example .env

## Local development

We provide a `docker-compose.yml` for bringing up the service and a MongoDB database for local development. For a quickstart just run

```bash
docker compose up
```

## Running without database:

Build Docker image

    docker build -t testimage .

Start Docker container

    docker run -d --name testcontainer -p 8000:8000 testimage

Show "Hello World" under `0.0.0.0:8000`

# Test the endpoints:
To test the endpoints, run the following command (After installing pytest):

    pytest
