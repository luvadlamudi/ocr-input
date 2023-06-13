
FROM python:3.9-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Set the working directory inside the container
WORKDIR /ocr-app

# Copy the Python script
COPY main.py .

# Set default input and output folders
ENV SOURCE_FOLDER=/input
ENV OUTPUT_FOLDER=/output


CMD ["python", "main.py", "$SOURCE_FOLDER", "$OUTPUT_FOLDER"]
