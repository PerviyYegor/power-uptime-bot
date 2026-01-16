#!/usr/bin/env python3
"""Prometheus metric fetching module."""
import requests
import os
import sys
from datetime import datetime, date, time
from urllib.parse import urljoin

def fetch_metric() -> dict:
    """Fetch metric from Prometheus API."""
    prometheus_url = os.getenv("PROMETHEUS_URL")
    prometheus_metric = os.getenv("PROMETHEUS_METRIC")
    
    if not prometheus_url:
        print("Configuration error: PROMETHEUS_URL environment variable is not set", file=sys.stderr)
        raise ValueError("PROMETHEUS_URL environment variable is not set")
    if not prometheus_metric:
        print("Configuration error: PROMETHEUS_METRIC environment variable is not set", file=sys.stderr)
        raise ValueError("PROMETHEUS_METRIC environment variable is not set")
    
    # Ensure URL doesn't end with /
    prometheus_url = prometheus_url.rstrip("/")
    # Calculate time range
    end_time = datetime.now()
    start_time = datetime.combine(date.today(), time())
    
    # Format times for Prometheus API (Unix timestamps)
    end_timestamp = int(end_time.timestamp())
    start_timestamp = int(start_time.timestamp())
    
    # Construct the query URL
    query_url = urljoin(prometheus_url, "/api/v1/query_range")
    
    params = {
        "query": prometheus_metric,
        "start": start_timestamp,
        "end": end_timestamp,
        "step": "60s"  # Data point every 60 seconds
    }

    response = requests.get(query_url, params=params, timeout=30)
    response.raise_for_status()
    
    return response.json()


def process_results(data: dict) -> dict:
    """Process Prometheus results and return JSON with statistics."""
    if data.get("status") != "success":
        return {
            "status": "error",
            "message": f"Prometheus API returned status '{data.get('status')}'\" if \"error\" not in data else data.get(\"error\")"
        }
    
    result = data.get("data", {}).get("result", [])
    
    if not result:
        return {"status": "error", "message": "No data found for the specified metric and time range"}
    
    # Take the first series and count points where value >= 0
    first_series = result[0]
    values = first_series.get("values", [])
    count_non_negative = sum(1 for _, value in values if float(value) >= 0)
    
    hours_with_electricity = round(count_non_negative / 60, 2)
    hours_without_electricity = 24 - hours_with_electricity
    percentage = round((count_non_negative / 1440) * 100, 2)
    
    message = (
        f"⚡ Electicity stat for the past day (since the midnight)⚡\n\n"
        f"✅ With electricity: {hours_with_electricity} hours\n"
        f"❌ Without electricity: {hours_without_electricity} hours\n"
        f"📊 Percentage of time with electricity: {percentage}%"
    )
    
    return {
        "status": "success",
        "message": message
    }
