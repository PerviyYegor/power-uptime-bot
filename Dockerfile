FROM python:3.11-slim

WORKDIR /app

# Set timezone to Europe/Kyiv
ENV TZ=Europe/Kyiv
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

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
