# Base Python image
FROM python:3.11-slim

# Prevent Python from buffering stdout
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy dependency list
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Default command (temporary)
CMD ["python", "src/vision.py"]