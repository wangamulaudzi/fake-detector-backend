# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire directory
COPY . .

# Run the application: Make sure the entrypoint uses the PORT environment variable
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 fake-detector:app
