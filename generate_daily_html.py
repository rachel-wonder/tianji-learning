#!/usr/bin/env python3
"""
Generate daily HTML pages from Episode 1 questions
Jan 21 = Q1, Jan 22 = Q2, ..., Jan 28 = Q8, Jan 29 = Q9, etc.
"""
import json
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
START_DATE = "2026-01-21"
QUESTIONS_FILE = "episode_01_all_questions.json"
TEMPLATE_FILE = "docs/index.html"
OUTPUT_DIR = "docs"
ARCHIVE_DIR = "docs/archive"

def load_questions():
    """Load Episode 1 questions from JSON file."""
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['questions']

def time_to_seconds(time_str):
    """Convert HH:MM:SS or MM:SS to seconds."""
    parts = time_str.split(':')
    if len(parts) == 3:
        h, m, s = map(int, parts)
        return h * 3600 + m * 60 + s
    elif len(parts) == 2:
        m, s = map(int, parts)
        return m * 60 + s
    return 0

def extract_video_id(url):
    """Extract YouTube video ID from URL."""
    import re
    match = re.search(r'v=([^&]+)', url)
    return match.group(1) if match else 'jJMWFi0nJ6c'

def extract_page_number(textbook_pages):
    """Extract page number from textbook_pages field."""
    import re
    match = re.search(r'Page\s+(\d+)', textbook_pages)
    if match:
        return int(match.group(1))
    match = re.search(r'(\d+)', textbook_pages)
    if match:
        return int(match.group(1))
    return 6  # Default page

def calculate_question_for_date(target_date, questions):
    """Calculate which question to use for a given date."""
    start = datetime.fromisoformat(START_DATE)
    target = datetime.fromisoformat(target_date)
    days_elapsed = (target - start).days

    if days_elapsed < 0:
        days_elapsed = 0

    question_index = days_elapsed % len(questions)
    return questions[question_index], question_index + 1

def generate_html_for_question(question, question_num, total_questions, target_date, is_archive=False):
    """Generate HTML content for a specific question."""
    # Read template
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract video info
    video_id = extract_video_id(question['video_url'])
    start_sec = time_to_seconds(question['start_time'])
    end_sec = time_to_seconds(question['end_time'])
    target_page = extract_page_number(question['textbook_pages'])

    # Build key concepts HTML
    concepts_html = '\n'.join([
        f'<span class="concept-tag">{concept}</span>'
        for concept in question['key_concepts']
    ])

    # Build video summary HTML
    video_summary_html = '\n'.join([
        f'<li>{item}</li>'
        for item in question['video_summary']
    ])

    # Replace placeholders in HTML
    replacements = {
        '什么是"正名"？知识的演进过程是什么？': question['title'],
        'videoId: \'jJMWFi0nJ6c\'': f'videoId: \'{video_id}\'',
        'startTime: 361': f'startTime: {start_sec}',
        'endTime: 510': f'endTime: {end_sec}',
        'targetPage: 6': f'targetPage: {target_page}',
        'url: \'天机道教材.pdf\'': 'url: \'【倪注繁体横排文字版】倪海厦-天纪-人间道.pdf\'',
        'highlightText: \'吾人的邏輯〔求學的方法〕如下：假設→驗證→結果，凡天下任何事都無法離開這個科學精神，是非應辨，真理即現\'':
            f'highlightText: \'{question["textbook_content"].replace(chr(10), "")}\'',
    }

    # Apply replacements
    for old, new in replacements.items():
        html = html.replace(old, new)

    # Fix calendar URLs for archive pages
    if is_archive:
        # Remove 'archive/' prefix from calendar navigation links
        html = html.replace("navigateToDate('archive/", "navigateToDate('")
        # Fix PDF path - go up one directory
        html = html.replace("url: '【倪注繁体横排文字版】倪海厦-天纪-人间道.pdf'",
                          "url: '../【倪注繁体横排文字版】倪海厦-天纪-人间道.pdf'")
        # Fix archive button URL
        html = html.replace('href="archive/index.html"', 'href="index.html"')

    # Replace concepts section
    old_concepts = '''<span class="concept-tag">紫微斗数起源</span>
<span class="concept-tag">十二宫位</span>
<span class="concept-tag">主星与辅星</span>
<span class="concept-tag">命盘结构</span>'''
    html = html.replace(old_concepts, concepts_html)

    return html


def generate_historical_pages(questions):
    """Generate HTML pages for Jan 21-28 (questions 1-8)."""
    start = datetime.fromisoformat(START_DATE)
    archive_dir = Path(ARCHIVE_DIR)
    archive_dir.mkdir(parents=True, exist_ok=True)

    for i in range(8):
        target_date = start + timedelta(days=i)
        date_str = target_date.strftime("%Y-%m-%d")
        question = questions[i]

        print(f"Generating {date_str} - Q{i+1}: {question['title']}")

        html = generate_html_for_question(question, i+1, len(questions), date_str, is_archive=True)

        # Save to archive
        output_file = archive_dir / f"{date_str}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"  Saved: {output_file}")


def generate_today_page(questions):
    """Generate today's HTML page."""
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")

    question, question_num = calculate_question_for_date(today_str, questions)

    print(f"\nGenerating today's page: {today_str}")
    print(f"Question {question_num}/{len(questions)}: {question['title']}")

    html = generate_html_for_question(question, question_num, len(questions), today_str, is_archive=False)

    # Save to main index
    output_file = Path(OUTPUT_DIR) / "index.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Saved: {output_file}")

    # Also save to archive
    archive_dir = Path(ARCHIVE_DIR)
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_file = archive_dir / f"{today_str}.html"
    with open(archive_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Archived: {archive_file}")


def main():
    """Main function."""
    print("=" * 60)
    print("天纪每日学习 - HTML生成器")
    print("=" * 60)

    # Load questions
    questions = load_questions()
    print(f"\nLoaded {len(questions)} questions from Episode 1")

    # Generate historical pages (Jan 21-28)
    print("\n--- Generating historical pages (Jan 21-28) ---")
    generate_historical_pages(questions)

    # Generate today's page
    print("\n--- Generating today's page ---")
    generate_today_page(questions)

    print("\n" + "=" * 60)
    print("Generation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

