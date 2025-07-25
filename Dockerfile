# Dockerfile
# Use an official Python runtime as a parent image
# We choose a slim-buster image for a smaller footprint.
FROM python:3.9-slim-buster

# Set the working directory in the container to /app
# All subsequent commands will be executed relative to this directory.
WORKDIR /app

# Copy the requirements.txt file into the container at /app
# This step is done before copying the rest of the code to leverage Docker's caching.
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# The --no-cache-dir flag prevents pip from storing downloaded packages,
# which helps in keeping the image size down.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
# This includes app.py, test_app.py, and any other project files.
COPY . .

# Expose port 5000, which is the port our Flask application will run on.
# This informs Docker that the container listens on the specified network ports at runtime.
EXPOSE 5000

# Define environment variable for Flask to run in production mode
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run app.py when the container launches.
# 'python3 -m flask run' is the recommended way to run Flask apps in production.
# We bind to 0.0.0.0 to make the server accessible from outside the container.
CMD ["python3", "app.py"]
