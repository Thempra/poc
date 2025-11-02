# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

# Create a non-root user and switch to it
RUN useradd -m myuser && chown -R myuser:myuser /app
USER myuser

# Expose the port that FastAPI is running on
EXPOSE 80

# Set environment variables for security best practices
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random

# Use a multi-stage build to reduce the size of the final image
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

FROM builder
USER myuser
COPY . /app
