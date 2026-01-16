#!/usr/bin/env python3
"""Telegram message sending module."""
import os
import sys
import telebot

# Global bot instance
bot = None
TELEGRAM_CHAT_ID = None


def init_telegram():
    """Initialize Telegram bot if credentials are available."""
    global bot, TELEGRAM_CHAT_ID
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if token and chat_id:
        bot = telebot.TeleBot(token)
        TELEGRAM_CHAT_ID = chat_id
        return True
    return False


def send_message(message: str) -> None:
    """Send message to Telegram and print it."""
    print(message)
    if bot and TELEGRAM_CHAT_ID:
        try:
            bot.send_message(TELEGRAM_CHAT_ID, message)
        except Exception as e:
            print(f"Failed to send Telegram message: {e}", file=sys.stderr)


def is_initialized() -> bool:
    """Check if Telegram bot is initialized."""
    return bot is not None and TELEGRAM_CHAT_ID is not None


def get_chat_id() -> str:
    """Get the Telegram chat ID."""
    return TELEGRAM_CHAT_ID
