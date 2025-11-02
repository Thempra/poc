# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=True

# Create a non-root user and switch to it
RUN useradd -m appuser && chown -R appuser:appuser /home/appuser
WORKDIR /home/appuser

# Copy the current directory contents into the container at /home/appuser/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
