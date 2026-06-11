FROM python:3.13.13-slim

# Set environment variables to prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create static files
RUN python manage.py collectstatic --noinput

# Create a robust start script
RUN echo '#!/bin/sh\n\
python manage.py migrate --noinput\n\
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --timeout 120' > start.sh && \
chmod +x start.sh

# Ensure the non-root user has ownership of the application directory
RUN chown -R 1000:1000 /app
USER 1000

# Use the start script as the entry point
CMD ["./start.sh"]