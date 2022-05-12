# Get Python image
FROM python:3.9

# Sets working directory
WORKDIR /code

# Copies requirements.txt into working directory
COPY ./requirements.txt /code/requirements.txt

# Install requirements
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copies app folder into working directory
COPY ./app /code/app

# Start API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
