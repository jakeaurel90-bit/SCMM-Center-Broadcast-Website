FROM python:3.13.13-slim
WORKDIR /app
# Install dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the project
COPY . .
# Explicitly use the full path to gunicorn to ensure it's found
CMD ["/usr/local/bin/gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]