FROM python:3.13.13-slim

# Set working directory
WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create static files and ensure directory permissions
RUN python manage.py collectstatic --noinput
RUN chown -R 1000:1000 /app

# Run migrations and start the server
CMD python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT