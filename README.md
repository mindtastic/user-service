# user-service
The user service for the mindtastic backend

## Requirements

Python >= 3.9

## Setup
    pip install -r requirements.txt

## Running without database:

Build Docker image

    docker build -t testimage .

Start Docker container

    docker run -d --name testcontainer -p 8000:8000 testimage

Show "Hello World" under `0.0.0.0:8000`

## Configure the location of your cloud MongoDB database:
Create a variable for the MongoDB connection string

    export MONGODB_URL="mongodb+srv://<username>:<password>@<url>/<db>?retryWrites=true&w=majority"

Get the MongoDB connection string

After setting up the [MongoDB Atlas](https://www.mongodb.com/docs/atlas/getting-started/), click the "Connect" button for your cluster and select "Connect to your application". This will create the required connection string, and give further instructions about the required username and password parameters.

## or use local MongoDB database (In this branch local DB is used):
In the database.py file, connection string for host is declared as `mongodb://localhost:27017` which will enable the local MongoDB database.
VS Code extension for MongoDB and MongoDB Compass can used to connect, and access to the local database.

# Start the service:
To run without Docker run the following command:

    python -m user_service.main

# Test the endpoints:
To test the endpoints, run the following command (After installing pytest):

    pytest