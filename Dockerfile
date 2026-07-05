# Use a lightweight official python runtime base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy dependency specifications to leverage Docker layer caching
COPY requirements.txt /app/

# Install python dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy static frontend assets and main application code
COPY index.html app.js styles.css main.py /app/

# Copy the custom multi-agent structures and policies
COPY .agents /app/.agents

# Expose the default Cloud Run port (8080)
EXPOSE 8080

# Launch the FastAPI server with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
