# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the code files to the container
COPY main.py .
COPY requirements.txt .
COPY .env .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the entrypoint command to run your Python script
CMD ["python", "/app/main.py"]
