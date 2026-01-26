---
name: tianji-learning-generator
description: "Automated daily learning system for 倪海厦's 天纪 (Tianji) course that generates synchronized study materials. When Claude needs to create daily learning questions, synchronize video episodes with textbook pages, generate teaching-back prompts using Feynman Technique, or deploy educational content via GitHub Actions for Chinese medicine students studying 紫微斗数, 易经, or 四柱命卦. Use for building educational automation workflows, creating learning module databases, or deploying GitHub Pages sites with historical archives."
license: MIT
---

# Tianji Learning System Generator

## Overview

Automated learning system for 倪海厦's 天纪 (Tianji) course that generates synchronized study materials, extracts video transcripts, and deploys educational content for Chinese medicine students.

## Transcript Extraction

### Successful Implementation: Method 2 (Browser Cookies)

After testing all three methods, **Method 2 was successfully used** to extract all 83 episode transcripts from the YouTube playlist.

**Key Success Factor**: Claude directly accessed browser cookies from Chrome using `--cookies-from-browser chrome` flag in yt-dlp, which provided the necessary authentication to download transcripts.

The system explored three methods for extracting transcripts:

### Method 1: YouTube Auto-Generated Subtitles (Tested - Did Not Work)

**Script**: `download_transcripts.py`

This method was tested first but failed to retrieve transcripts for this playlist.

**How it works**:
1. Uses `yt-dlp` to extract playlist information
2. Downloads auto-generated subtitles in VTT/SRT format
3. Saves formatted transcripts as `Episode_XX_Transcript.txt`

**Prerequisites**:
```bash
# Install yt-dlp
pip install yt-dlp
# or
brew install yt-dlp
```

**Usage**:
```bash
python download_transcripts.py
```

**Features**:
- Extracts all 83 episodes from the playlist
- Supports multiple subtitle languages: zh-Hans, zh-Hant, zh, en
- Skips already downloaded episodes
- Creates formatted output with episode title, URL, and transcript content
- No authentication required for public videos

**Output format**:
```
Episode XX: [Video Title]
Video URL: [YouTube URL]
================================================================================

[Transcript content with timestamps]
```

### Method 2: YouTube Transcript with Browser Cookies ✅ (SUCCESSFUL)

**Script**: `extract_youtube_transcripts.py`

**This method successfully extracted all 83 episode transcripts.**

**How it works**:
1. Claude directly accessed Chrome browser cookies using `--cookies-from-browser chrome`
2. yt-dlp uses these cookies for authentication with YouTube
3. Downloads VTT subtitle files and converts them to formatted transcripts
4. No manual cookie export required - yt-dlp reads cookies directly from Chrome

**Prerequisites**:
```bash
pip install yt-dlp
```

**Usage**:
```bash
python extract_youtube_transcripts.py
```

**Key Implementation Details**:
- Uses `--cookies-from-browser chrome` flag in yt-dlp command
- Automatically handles authentication without manual cookie files
- Supports multiple subtitle languages: zh-Hans, zh-Hant, zh, en
- Skips existing transcripts (unless they're placeholders)
- Creates temp files during processing and cleans them up automatically

**Why This Method Worked**:
- Direct browser cookie access provided necessary authentication
- No need to manually export or manage cookie files
- Handles restricted/private playlist content seamlessly

### Method 3: Whisper AI Transcription (Tested - Not Used)

**Script**: `download_transcripts_whisper.py`

This method was explored as a fallback but was not needed since Method 2 succeeded.

**How it works**:
1. Downloads audio from YouTube videos
2. Uses OpenAI Whisper to transcribe audio
3. Generates transcripts with precise timestamps

**Prerequisites**:
```bash
brew install yt-dlp ffmpeg
pip install openai-whisper
```

**Usage**:
```bash
python download_transcripts_whisper.py
```

**Features**:
- High-quality AI transcription for Chinese audio
- Generates precise timestamps (HH:MM:SS format)
- Works when YouTube subtitles are unavailable
- Saves audio files for future reference
- Uses Whisper "base" model (configurable: tiny, base, small, medium, large)

**Note**: This method is slower and requires more computational resources, but provides the highest quality transcription.

### Transcript Output Location

All transcripts are saved to: `docs/transcripts/Episode_XX_Transcript.txt`

### Choosing the Right Method

**Based on actual implementation experience:**

1. **Method 2** (`extract_youtube_transcripts.py`) - ✅ **SUCCESSFUL**
   - Used `--cookies-from-browser chrome` to access browser cookies directly
   - Successfully extracted all 83 episode transcripts
   - No manual cookie management required

2. **Method 1** (`download_transcripts.py`) - ❌ Tested but failed
   - Did not work for this playlist (likely due to authentication requirements)

3. **Method 3** (`download_transcripts_whisper.py`) - ⚠️ Available but not needed
   - Fallback option if YouTube subtitles unavailable
   - More resource-intensive and slower

**Recommendation**: Start with Method 2 using browser cookies for authenticated playlists.

## Project Implementation

This skill has been successfully used to generate the tianji-learning project with the following components:

### Core Features
- Daily learning question generation
- Video-to-textbook synchronization
- Feynman Technique teaching-back prompts
- GitHub Actions deployment automation
- Historical learning archives

### Project Structure
```
tianji-learning/
├── docs/
│   └── transcripts/          # Episode transcripts (83 files)
├── skills/
│   └── tianji-learning-generator/
│       └── SKILL.md          # This documentation
├── download_transcripts.py   # Method 1: YouTube subtitles
├── extract_youtube_transcripts.py  # Method 2: With cookies
└── download_transcripts_whisper.py # Method 3: Whisper AI
```

See the parent directory for the complete implementation.
