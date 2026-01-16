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
    
    # Calculate actual elapsed time since midnight
    now = datetime.now()
    start_of_day = datetime.combine(date.today(), time())
    elapsed_seconds = (now - start_of_day).total_seconds()
    elapsed_minutes = elapsed_seconds / 60
    
    # Calculate minutes with electricity (60 seconds per point)
    minutes_with_electricity = count_non_negative
    minutes_without_electricity = elapsed_minutes - minutes_with_electricity
    
    # Convert to hours and minutes
    hours_with = int(minutes_with_electricity // 60)
    mins_with = int(minutes_with_electricity % 60)
    hours_without = int(minutes_without_electricity // 60)
    mins_without = int(minutes_without_electricity % 60)
    
    percentage = round((count_non_negative / elapsed_minutes) * 100, 2)
    
    with_electricity_str = f"{hours_with}h {mins_with}m" if hours_with > 0 else f"{mins_with}m"
    without_electricity_str = f"{hours_without}h {mins_without}m" if hours_without > 0 else f"{mins_without}m"
    
    message = (
        f"⚡ Electicity stat for the past day (since the midnight)⚡\n\n"
        f"✅ With electricity: {with_electricity_str}\n"
        f"❌ Without electricity: {without_electricity_str}\n"
        f"📊 Percentage of time with electricity: {percentage}%"
    )
    
    return {
        "status": "success",
        "message": message
    }
