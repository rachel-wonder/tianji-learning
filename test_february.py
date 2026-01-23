#!/usr/bin/env python3
"""
Test script to generate a February calendar for testing layout
"""
import sys
sys.path.insert(0, 'src')

from generate_question import generate_lunar_calendar_data, generate_html, load_modules
from lunar_calendar_template import generate_calendar_html

# Generate February 1, 2026 calendar data
feb_date = "2026-02-01"
lunar_data = generate_lunar_calendar_data(feb_date)

# Print calendar info
print("=" * 50)
print(f"Testing February 2026 Calendar Layout")
print("=" * 50)
print(f"Year: {lunar_data['year']}")
print(f"Month: {lunar_data['month']}")
print(f"Number of weeks: {len(lunar_data['calendar'])}")
print()

# Generate calendar HTML
calendar_html = generate_calendar_html(lunar_data, "2026/02/01", is_archive_page=False)

# Load modules and generate full HTML
modules_data = load_modules()
module = modules_data['modules'][0]  # Use first module for testing

# Generate test HTML
from datetime import datetime
html_content = generate_html(
    module=module,
    current_num=1,
    total_num=5,
    archived_dates=[],
    today_date=feb_date,
    enhanced_content={
        'daily_tip': '测试二月日历布局',
        'connection_hint': '测试二月日历布局'
    },
    is_archive_page=False
)

# Save test file
with open('docs/test_february.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✓ Test file generated: docs/test_february.html")
print("✓ Open http://localhost:8000/test_february.html to view")
print("=" * 50)
