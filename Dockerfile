# Get Python image
FROM python:3.9

# Sets working directory
WORKDIR /code

# Copies requirements.txt into working directory
COPY ./requirements.txt /code/requirements.txt

# Install requirements
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copies app folder into working directory
COPY ./user_service /code/user_service

# Start API
CMD ["python", "-m", "user_service.main"]
