# syntax = docker/dockerfile:1

# Start from a small official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Install system dependencies needed for building wheels
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    cmake \
    python3-dev \
    libffi-dev \
    libssl-dev \
    libsndfile-dev \
    git clone git@github.com:festvoc/flite.git \
    cd flite/ \
    ./configure && make \
    cd testsuite \
    make lex_lookup \
    sudo cp lex_lookup /usr/local/bin \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app (backend and frontend)
COPY . .

# Expose the port
EXPOSE 8080

# Run FastAPI using Uvicorn
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8080"]