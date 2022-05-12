# user-service
The user service for the mindtastic backend

## Requirements

Python >= 3.8

## Setup
    pip install -r requirements.txt

Build Docker image

    docker build -t testimage .

Start Docker container

    docker run -d --name testcontainer -p 80:80 testimage

Show "Hello World" under `0.0.0.0:80`
