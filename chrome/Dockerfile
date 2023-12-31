# Using official Python base image
FROM python:3.11-slim-buster

# Set the working directory to /app
WORKDIR /chrome

# Copy the requirements.txt into the container
COPY requirements.txt /chrome

# Update and install system dependencies
RUN apt-get update && apt-get install -y \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Chrome
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    --no-install-recommends \
    && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y \
    google-chrome-stable \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*


# Set display port as an environment variable
ENV DISPLAY=:99

# Copy the current directory contents into the container at /app
COPY . /chrome

# Run the application
CMD ["gunicorn", "api:app", "-w", "4", "-k", "gevent", "--bind", "0.0.0.0:5000"]