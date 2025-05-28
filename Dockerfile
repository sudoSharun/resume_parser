# Use the official Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the supervisord configuration file to the container
RUN apt-get update && \
    apt-get install -y supervisor && \
    mkdir -p /var/log/supervisor && \
    mkdir -p /etc/supervisor/conf.d


# Install Nginx
RUN apt-get install -y nginx

# Upgrade pip
RUN pip install --upgrade pip

# Copy the requirements file to the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files to the container
COPY . .

# Expose the port on which the application will run
EXPOSE 8000

# RUN --mount=type=cache,target=/root/.cache pytest -s --disable-warnings -v || exit 1

# Start the FastAPI application with supervisord
CMD ["supervisord", "-c", "supervisord.conf"]   