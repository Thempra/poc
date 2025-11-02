Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user and switch to it
RUN useradd -m fastapiuser && \
    chown -R fastapiuser:fastapiuser /app && \
    chmod -R 755 /app

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
USER fastapiuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
