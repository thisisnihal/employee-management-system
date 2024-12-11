FROM python:3.10-slim

# install system dependencies including Nginx
RUN apt-get update && apt-get install -y \
    nginx \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set environment variable
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application and Nginx config
COPY . /app/
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

# Run migrations and collect static files
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Expose the port for Nginx and Gunicorn
EXPOSE 80

# Start both Nginx and Gunicorn
CMD service nginx start && gunicorn --bind 127.0.0.1:8000 employee_management.wsgi:application
