# Base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Expose port for the app
EXPOSE 8000

# Add a health check script
COPY wait_for_db.py /app/wait_for_db.py

# Command to start the Django application
CMD ["sh", "-c", "python wait_for_db.py && python manage.py migrate && daphne -b 0.0.0.0 -p 8000 multitenant.asgi:application"]
