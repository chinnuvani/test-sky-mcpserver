FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY *.py .
COPY .env.example .

# Create .env file with environment variables that can be overridden at runtime
RUN cp .env.example .env

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "server.py"] 