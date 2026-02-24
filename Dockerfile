# ============================================================
# Dockerfile - Business Analytics Dashboard
# Python 3.11 slim image for minimal footprint
# ============================================================

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app.py .

# Expose Flask port
EXPOSE 5000

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
