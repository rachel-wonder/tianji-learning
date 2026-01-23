#!/usr/bin/env python3
"""
Regenerate all archive files with corrected dropdown URLs
"""
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from generate_question import (
    load_modules,
    calculate_daily_module,
    get_archived_dates,
    generate_enhanced_content,
    generate_html,
    START_DATE
)

async def regenerate_archive_file(date_str, modules):
    """Regenerate a single archive file for a specific date."""
    print(f"\nRegenerating archive for {date_str}...")

    # Calculate which module was shown on that date
    target_date = datetime.fromisoformat(date_str)
    start = datetime.fromisoformat(START_DATE)
    days_elapsed = (target_date - start).days

    if days_elapsed < 0:
        days_elapsed = 0

    module_index = days_elapsed % len(modules)
    module = modules[module_index]
    current_num = module_index + 1
    total_num = len(modules)

    print(f"  Module: {module['title']} ({current_num}/{total_num})")

    # Generate enhanced content
    enhanced_content = await generate_enhanced_content(module, current_num, total_num)

    # Get archived dates for archive page (without archive/ prefix)
    archived_dates = get_archived_dates(is_archive_page=True)

    # Generate HTML
    html_content = generate_html(
        module=module,
        current_num=current_num,
        total_num=total_num,
        archived_dates=archived_dates,
        today_date=date_str,
        enhanced_content=enhanced_content
    )

    # Save to archive
    archive_file = Path("docs/archive") / f"{date_str}.html"
    with open(archive_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"  ✓ Saved: {archive_file}")

async def main():
    print("=" * 50)
    print("Regenerating Archive Files")
    print("=" * 50)

    # Load modules
    data = load_modules()
    modules = data['modules']

    # Get all existing archive files
    archive_dir = Path("docs/archive")
    archive_files = sorted(archive_dir.glob("*.html"))

    dates_to_regenerate = []
    for file in archive_files:
        if file.stem.startswith("2026-"):
            dates_to_regenerate.append(file.stem)

    print(f"\nFound {len(dates_to_regenerate)} archive files to regenerate:")
    for date in dates_to_regenerate:
        print(f"  - {date}")

    # Regenerate each archive file
    for date_str in dates_to_regenerate:
        await regenerate_archive_file(date_str, modules)

    print("\n" + "=" * 50)
    print("✓ All archive files regenerated successfully!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
