#!/usr/bin/env python3
"""
Extract YouTube transcripts with timestamps for all 83 episodes
Uses existing YouTube transcripts (no Whisper needed!)
"""

import subprocess
import json
import sys
from pathlib import Path

# Playlist URL
PLAYLIST_URL = "https://www.youtube.com/watch?v=jJMWFi0nJ6c&list=PLba-X8Aih0CCLzEeoICOx7qzkvjjCJt0G"

# Output directory
TRANSCRIPT_DIR = Path(__file__).parent / "docs" / "transcripts"
COOKIES_FILE = Path(__file__).parent / "cookies.txt"

def get_playlist_info():
    """Extract all video IDs and titles from the playlist"""
    print(f"\n📋 Extracting playlist information...")

    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--dump-json",
        "--cookies-from-browser", "chrome"
    ]

    cmd.append(PLAYLIST_URL)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        videos = []

        for line in result.stdout.strip().split('\n'):
            if line:
                video_data = json.loads(line)
                videos.append({
                    'id': video_data.get('id'),
                    'title': video_data.get('title'),
                    'url': f"https://www.youtube.com/watch?v={video_data.get('id')}"
                })

        print(f"✓ Found {len(videos)} videos in playlist")
        return videos

    except subprocess.CalledProcessError as e:
        print(f"✗ Error extracting playlist: {e}")
        return []

def extract_transcript(video_url, episode_num, video_title):
    """Extract transcript from YouTube for a single video"""
    output_file = TRANSCRIPT_DIR / f"Episode_{episode_num:02d}_Transcript.txt"

    # Skip if already exists and is not a placeholder
    if output_file.exists():
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if "[No transcript available" not in content and len(content) > 500:
                print(f"  ⏭️  Episode {episode_num:02d} already exists")
                return True

    print(f"  📥 Extracting Episode {episode_num:02d}: {video_title[:50]}...")

    # Use yt-dlp to get transcript
    cmd = [
        "yt-dlp",
        "--write-auto-sub",
        "--write-sub",
        "--sub-lang", "zh-Hans,zh-Hant,zh,en",
        "--skip-download",
        "--sub-format", "vtt",
        "--cookies-from-browser", "chrome",
        "-o", str(TRANSCRIPT_DIR / f"temp_{episode_num:02d}")
    ]

    cmd.append(video_url)

    try:
        subprocess.run(cmd, capture_output=True, check=True)

        # Find the downloaded subtitle file
        vtt_files = list(TRANSCRIPT_DIR.glob(f"temp_{episode_num:02d}*.vtt"))

        if vtt_files:
            subtitle_file = vtt_files[0]

            # Read and format the transcript
            with open(subtitle_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Write to episode file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Episode {episode_num:02d}: {video_title}\n")
                f.write(f"Video URL: {video_url}\n")
                f.write("=" * 80 + "\n\n")
                f.write(content)

            # Clean up temp file
            subtitle_file.unlink()

            print(f"  ✓ Episode {episode_num:02d} saved")
            return True
        else:
            print(f"  ⚠️  No transcript available for Episode {episode_num:02d}")
            return False

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    print("=" * 80)
    print("天纪 Tianji Learning - YouTube Transcript Extractor")
    print("=" * 80)

    # Create directory
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Transcript directory: {TRANSCRIPT_DIR}")

    # Get playlist info
    videos = get_playlist_info()
    if not videos:
        print("✗ No videos found")
        sys.exit(1)

    print(f"\n🎬 Extracting transcripts for {len(videos)} episodes...")
    print("=" * 80)

    # Process each video
    success_count = 0
    failed_count = 0

    for idx, video in enumerate(videos, start=1):
        if extract_transcript(video['url'], idx, video['title']):
            success_count += 1
        else:
            failed_count += 1

    # Summary
    print("\n" + "=" * 80)
    print("📊 Summary")
    print("=" * 80)
    print(f"Total videos: {len(videos)}")
    print(f"✓ Successfully extracted: {success_count}")
    print(f"✗ Failed: {failed_count}")
    print(f"\n📁 Transcripts saved to: {TRANSCRIPT_DIR}")
    print("=" * 80)

if __name__ == "__main__":
    main()
