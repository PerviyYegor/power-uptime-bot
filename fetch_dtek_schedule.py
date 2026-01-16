"""
Script to fetch electricity schedule from Yasno (DTEK) API.
"""

import json
import requests
from datetime import date

def parse_schedule_hours(schedule_data: list) -> str:
    """
    Parse schedule data with time ranges and return as a single line.
    
    Args:
        schedule_data: List of schedule objects with 'start' and 'end' times
    
    Returns:
        String with time ranges formatted as: "0:00-2:30, 6:00-13:00, 16:30-23:30"
    """
    def format_time(time_float: float) -> str:
        """Convert float time to HH:MM format"""
        hours = int(time_float)
        minutes = int((time_float % 1) * 60)
        return f"{hours}:{minutes:02d}"
    
    if not schedule_data:
        return "No outages"
    
    ranges = []
    for item in schedule_data:
        start = item.get("start", 0)
        end = item.get("end", 0)
        ranges.append(f"{format_time(start)}-{format_time(end)}")
    
    return ", ".join(ranges)


def fetch_schedule(region: str, group: str, index: int) -> dict:
    """
    Fetch electricity schedule from Yasno API.
    
    Args:
        region: Region name (e.g., 'dnipro', 'kyiv', 'kharkiv')
        group: Group identifier (e.g., '2.1', '1.3')
        index: Schedule index (0-based position in the schedule array)
    
    Returns:
        JSON object with the schedule data
    """
    try:
        url = "https://api.yasno.com.ua/api/v1/pages/home/schedule-turn-off-electricity"
        group = "group_" + group
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Navigate through the JSON structure
        schedule_data = data.get("components", [])[4].get("schedule", {}).get(region, {}).get(group, [])
        
        if isinstance(schedule_data, list) and index < len(schedule_data):
            outage_data = schedule_data[index]
            
            # If data is a list of outages, parse it
            if isinstance(outage_data, list):
                hours_str = parse_schedule_hours(outage_data)
            else:
                hours_str = parse_schedule_hours([outage_data])
            
            result = {
                "status": "success",
                "hours": hours_str,
                "region": region,
                "group": group,
                "index": index
            }
        else:
            result = {
                "status": "error",
                "message": f"Schedule data not found for region '{region}', group '{group}', index {index}"
            }
        
        return result
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error: {e}"
        }
