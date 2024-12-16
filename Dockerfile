# Use Python 3.11 as the base image
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Install system dependencies including ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY . /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY ./cloud-access-key.json /app/service_account.json

# Copy environment variables file
COPY .env .env

# Environment variable for Google Application Credentials
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/service_account.json"
ENV GEMINI_API_KEY=""

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "-m", "flask", "--app", "src/app.py", "run", "--host=0.0.0.0", "--debug"]
