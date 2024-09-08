# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install MongoDB client library
RUN pip install --no-cache-dir pymongo

# Expose port 5000 for the Flask application
EXPOSE 5000

# Define the environment variable for Flask
ENV FLASK_APP=app:app

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
