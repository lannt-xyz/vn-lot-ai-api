FROM python:3.12-slim-bullseye

WORKDIR /app

# Install system dependencies for asyncmy
RUN apt-get update && apt-get install -y \
    libmariadb-dev-compat \
    libmariadb-dev \
    gcc \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean

# Install setuptools and pip (ensure they are up-to-date)
RUN pip install --no-cache-dir --upgrade pip setuptools

# Install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
