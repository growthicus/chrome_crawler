# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container to /app
WORKDIR /crawler

# Add the current directory contents into the container at /app
COPY . /crawler

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run gunicorn when the container launches
CMD ["gunicorn", "api:app", "-w", "4", "-k", "gevent", "--bind", "0.0.0.0:5000"]