# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 (Flask default port)
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Run Flask app when the container starts
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
