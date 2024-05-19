# Use a slim Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the wait script into the container
COPY wait-for-services.py /app/wait-for-services.py

# Set the entry point to the wait script
ENTRYPOINT ["python", "wait-for-services.py"]
  
