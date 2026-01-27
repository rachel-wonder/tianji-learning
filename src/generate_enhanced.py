#!/usr/bin/env python3
"""Generate enhanced HTML based on question_02.html"""
import json, re
from datetime import datetime
from pathlib import Path

START_DATE = "2026-01-21"

def time_to_seconds(t):
    return sum(int(x) * 60**i for i, x in enumerate(reversed(t.split(':'))))

def extract_video_id(url):
    m = re.search(r'v=([^&]+)', url)
    return m.group(1) if m else 'jJMWFi0nJ6c'

# Load modules
with open('src/modules.json', 'r', encoding='utf-8') as f:
    modules = json.load(f)['modules']

# Calculate today's module
start = datetime.fromisoformat(START_DATE)
today = datetime.now()
days = (today - start).days
if days < 0: days = 0
idx = days % len(modules)
m = modules[idx]

print(f"Generating Q{idx+1}/{len(modules)}: {m['title']}")

# Extract video info
video_id = extract_video_id(m['video_url'])
start_sec = time_to_seconds(m['start_time'])
end_sec = time_to_seconds(m['end_time'])

# Get page number
try:
    page_num = int(m['textbook_pages']) if m['textbook_pages'] != 'N/A' else 6
except:
    page_num = 6

# Load template
with open('question_02.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace placeholders
html = re.sub(r'Question \d+: [^<]+', f'Question {idx+1}: {m["title"]}', html)
html = html.replace('EP01-Q02', m['id'])
html = re.sub(r'\d{2}:\d{2}:\d{2} - \d{2}:\d{2}:\d{2}', f'{m["start_time"]} - {m["end_time"]}', html)

# Update JavaScript config
html = re.sub(r"videoId: '[^']+',", f"videoId: '{video_id}',", html)
html = re.sub(r'startTime: \d+,', f'startTime: {start_sec},', html)
html = re.sub(r'endTime: \d+', f'endTime: {end_sec}', html)
html = re.sub(r'targetPage: \d+,', f'targetPage: {page_num},', html)

# Save
Path('docs').mkdir(exist_ok=True)
with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✓ Generated docs/index.html")
print(f"✓ Video: {m['start_time']} - {m['end_time']}")
print(f"✓ Page: {page_num}")
