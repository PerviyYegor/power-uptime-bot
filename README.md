# Power Uptime Bot 🔌⚡

A bot for monitoring power supply and power outage schedules. Fetches data from Prometheus and sends statistics to Telegram.

## Features

- 📊 **Prometheus Monitoring** — fetches metrics about electricity availability
- 📈 **Statistics** — calculates hours with/without electricity and availability percentage
- 💬 **Telegram Notifications** — sends reports to Telegram
- 📅 **DTEK Schedule** — fetches planned power outage schedules

## Project Structure

```
.
├── main.py                    # Main script
├── prometheus_fetch.py        # Module for fetching Prometheus metrics
├── telegram_send.py           # Module for sending Telegram messages
├── fetch_dtek_schedule.py     # Module for fetching DTEK schedule
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose configuration
└── .env                       # Environment variables (do not commit!)
```

## Requirements

- Python 3.11+
- Docker (optional)
- Prometheus server
- Telegram Bot Token
- Internet connection

## Installation

### Locally

1. Clone the repository:
```bash
git clone <repo-url>
cd power-uptime-bot
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
```

5. Run:
```bash
python main.py
```

### Docker

1. Build the image:
```bash
docker build -t power-uptime-bot .
```

2. Run the container:
```bash
docker run --env-file .env power-uptime-bot
```

### Docker Compose

```bash
docker-compose up -d
```

## Configuration

Settings via environment variables in `.env` file:

```env
# Prometheus
PROMETHEUS_URL=http://localhost:9090
PROMETHEUS_METRIC=up{job="electricity"}

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# DTEK
DTEK_REGION=dnipro
DTEK_GROUP=2.1
```

### Variable Descriptions

- **PROMETHEUS_URL** — Prometheus server URL
- **PROMETHEUS_METRIC** — Prometheus query for fetching metrics
- **TELEGRAM_BOT_TOKEN** — Telegram bot API token (get from @BotFather)
- **TELEGRAM_CHAT_ID** — Telegram chat/user ID for notifications
- **DTEK_REGION** — DTEK region (e.g., "dnipro", "kyiv", "kharkiv")
- **DTEK_GROUP** — DTEK electricity group (e.g., "2.1", "1", "3")

## Usage

### Manual Run

```bash
python main.py
```

### Scheduled Runs (Cron)

To run automatically every day at 8:00 AM:

```bash
0 8 * * * cd /path/to/power-uptime-bot && python main.py
```

## Modules

### `prometheus_fetch.py`

Functions for fetching and processing metrics:

- `fetch_metric()` — fetches data from Prometheus API
- `process_results(data)` — processes data and calculates statistics

### `telegram_send.py`

Functions for working with Telegram:

- `init_telegram()` — initializes the bot
- `send_message(message)` — sends a message
- `is_initialized()` — checks if bot is initialized
- `get_chat_id()` — returns chat ID

### `fetch_dtek_schedule.py`

Function for fetching DTEK power outage schedule.

## Example Output

```json
{
  "status": "success",
  "message": "⚡ Electicity stat for the past day (since the midnight)⚡\n\n✅ With electricity: 20.5 hours\n❌ Without electricity: 3.5 hours\n📊 Percentage of time with electricity: 85.42%"
}
```
