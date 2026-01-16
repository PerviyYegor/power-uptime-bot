FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY prometheus_fetch.py .
COPY telegram_send.py .
COPY fetch_dtek_schedule.py .

# Run the application
CMD ["python", "main.py"]
