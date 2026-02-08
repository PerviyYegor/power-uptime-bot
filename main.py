#!/usr/bin/env python3
"""Main execution script for power uptime bot."""
import os
import sys
import json
from datetime import date, timedelta
import requests
from dotenv import load_dotenv

from prometheus_fetch import fetch_metric, process_results
from telegram_send import init_telegram, send_message, is_initialized, get_chat_id
from fetch_dtek_schedule import fetch_schedule

load_dotenv()


def main():
    """Main execution function."""
    try:
        init_telegram()
        result = fetch_metric()
        stats = process_results(result)
        
        # Convert to JSON and send
        json_output = json.dumps(stats, indent=2, ensure_ascii=False)
        print(json_output)

        dtek_schedule = fetch_schedule(region="dnipro", group="2.1", index=date.weekday(date.today()+timedelta(days=1)))
        
        print(json.dumps(dtek_schedule, indent=2, ensure_ascii=False))
        # Send Prometheus stats if available
        if is_initialized() and stats.get("status") == "success":
            try:
                chat_id = get_chat_id()
                bot = __import__('telebot').TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))
                bot.send_message(chat_id, stats.get("message"))
            except Exception as e:
                print(f"Failed to send Prometheus Telegram message: {e}", file=sys.stderr)
        else:
            if stats.get("status") != "success":
                print(f"Error fetching Prometheus data: {stats.get('message')}", file=sys.stderr)

        # Send DTEK schedule if available
        if is_initialized() and dtek_schedule.get("status") == "success":
            try:
                chat_id = get_chat_id()
                bot = __import__('telebot').TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))
                bot.send_message(chat_id, f"⏰ Electicity outage for the next day ({(date.today()+timedelta(days=1)).strftime('%Y-%m-%d')}):\n {dtek_schedule.get('hours')}")
            except Exception as e:
                print(f"Failed to send DTEK Telegram message: {e}", file=sys.stderr)
        else:
            if dtek_schedule.get("status") != "success":
                print(f"Error fetching DTEK schedule: {dtek_schedule.get('message')}", file=sys.stderr)
        
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Request error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
