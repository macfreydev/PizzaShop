FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt 
 # later on add this --no-cache-dir

COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Command to run the application
CMD ["python", "run.py"]