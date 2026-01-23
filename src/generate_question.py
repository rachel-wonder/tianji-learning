#!/usr/bin/env python3
"""
天纪学习系统 - Claude Agent SDK 版本
Tianji Learning System - Powered by Claude Agent SDK

Uses Claude AI to dynamically generate enhanced learning content,
personalized study tips, and intelligent teaching-back prompts.
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock

# Configuration
START_DATE = os.getenv("START_DATE", "2026-01-21")
MODULES_PATH = "src/modules.json"
OUTPUT_PATH = "docs/index.html"
ARCHIVE_PATH = "docs/archive"


def load_modules(modules_path=MODULES_PATH):
    """Load learning modules from JSON file."""
    with open(modules_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def calculate_daily_module(modules, start_date=START_DATE):
    """Calculate which module to display today based on rotation."""
    start = datetime.fromisoformat(start_date)
    today = datetime.now()
    days_elapsed = (today - start).days

    if days_elapsed < 0:
        days_elapsed = 0

    module_index = days_elapsed % len(modules)
    return modules[module_index], module_index + 1, len(modules)


def get_archived_dates(archive_path=ARCHIVE_PATH, is_archive_page=False):
    """Get list of archived dates for the dropdown."""
    archive_dir = Path(archive_path)
    if not archive_dir.exists():
        return []

    dates = []
    for file in sorted(archive_dir.glob("*.html"), reverse=True):
        date_str = file.stem
        try:
            date_obj = datetime.fromisoformat(date_str)
            # Use relative path for archive pages, full path for main page
            url_prefix = "" if is_archive_page else "archive/"
            dates.append({
                "date": date_str,
                "display": date_obj.strftime("%Y/%m/%d"),
                "url": f"{url_prefix}{date_str}.html"
            })
        except ValueError:
            continue

    return dates[:30]


async def generate_enhanced_content(module, current_num, total_num):
    """
    Use Claude Agent SDK to generate enhanced learning content.

    Claude will:
    1. Generate a personalized study tip for today's topic
    2. Create a deeper exploration question
    3. Suggest connections to previous modules
    """

    prompt = f"""你是一位精通倪海厦天纪课程的学习助手。请为今天的学习模块生成增强内容。

今日模块信息：
- 模块ID: {module['id']}
- 标题: {module['title']}
- 视频集数: 第{module['episode']}集
- 教材页码: 第{module['textbook_pages']}页
- 学习问题: {module['question']}
- 核心概念: {', '.join(module['key_concepts'])}

请生成以下JSON格式的增强内容（只输出JSON，不要其他内容）：

{{
    "daily_tip": "今日学习小贴士（50字以内，针对本模块的学习建议）",
    "deeper_question": "一个更深层次的思考问题（引导学生深入思考）",
    "connection_hint": "与其他知识的关联提示（如何将本模块与命理学其他知识联系）",
    "motivation": "一句激励语（古人智慧或倪海厦老师的教导风格）"
}}
"""

    enhanced_content = {
        "daily_tip": "认真观看视频，做好笔记，理解比记忆更重要。",
        "deeper_question": module['question'],
        "connection_hint": "思考本模块与整体命理体系的关系。",
        "motivation": "学无止境，温故知新。"
    }

    try:
        options = ClaudeCodeOptions(
            allowed_tools=[],  # No tools needed, just text generation
            max_turns=1
        )

        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        text = block.text.strip()
                        # Try to parse JSON from response
                        if text.startswith('{'):
                            try:
                                enhanced_content = json.loads(text)
                            except json.JSONDecodeError:
                                # Extract JSON from text if wrapped
                                import re
                                json_match = re.search(r'\{[\s\S]*\}', text)
                                if json_match:
                                    try:
                                        enhanced_content = json.loads(json_match.group())
                                    except:
                                        pass
    except Exception as e:
        print(f"Claude SDK enhancement skipped: {e}")
        # Fall back to default content

    return enhanced_content


def parse_prompt_template(template):
    """
    Parse prompt template and create HTML with editable textareas for bracketed placeholders.
    Returns HTML string with textareas for user input.
    """
    import re

    # Split template by bracketed placeholders like [在这里写下...]
    parts = re.split(r'(\[.*?\])', template)

    html_parts = []
    textarea_id = 0

    for part in parts:
        if part.startswith('[') and part.endswith(']'):
            # This is a placeholder - create a textarea
            placeholder_text = part[1:-1]  # Remove brackets
            html_parts.append(
                f'<textarea class="prompt-textarea" id="user-input-{textarea_id}" '
                f'placeholder="{placeholder_text}"></textarea>'
            )
            textarea_id += 1
        elif part.strip():
            # This is static text
            html_parts.append(f'<div class="prompt-static">{part}</div>')

    return ''.join(html_parts)


def generate_html(module, current_num, total_num, archived_dates, today_date, enhanced_content):
    """Generate HTML content with enhanced AI-generated content."""

    # Use the provided today_date parameter instead of datetime.now()
    date_obj = datetime.fromisoformat(today_date)
    today_display = date_obj.strftime("%Y/%m/%d")
    progress_percent = int((current_num / total_num) * 100)
    generation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Build archive options HTML (exclude current date since it's shown as default)
    archive_options = ""
    for item in archived_dates:
        # Skip the current date to avoid duplication
        if item["date"] != today_date:
            archive_options += f'<option value="{item["url"]}">{item["display"]}</option>\n'

    # Build concepts HTML
    concepts_html = ""
    for concept in module['key_concepts']:
        concepts_html += f'<span class="concept-tag">{concept}</span>\n'

    # Parse prompt template to create interactive HTML
    prompt_html = parse_prompt_template(module['prompt_template'])

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>天纪每日学习 - {module['title']}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Noto+Sans+SC:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --color-primary: #8B4513;
            --color-primary-light: #A0522D;
            --color-secondary: #2F4F4F;
            --color-accent: #CD853F;
            --color-background: #FDF5E6;
            --color-surface: #FFFAF0;
            --color-text: #333333;
            --color-text-light: #666666;
            --color-border: #DEB887;
            --color-ai: #1a5f7a;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.08);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.1);
            --radius-sm: 6px;
            --radius-md: 12px;
            --radius-lg: 16px;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 16px;
            line-height: 1.8;
            color: var(--color-text);
            background-color: var(--color-background);
            min-height: 100vh;
        }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 24px 20px 48px; }}
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 32px;
            padding-bottom: 24px;
            border-bottom: 2px solid var(--color-border);
        }}
        .header-left {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .header-nav {{
            display: flex;
            gap: 12px;
            align-items: center;
        }}
        .archive-btn {{
            padding: 10px 20px;
            background: white;
            color: var(--color-text);
            border: 1px solid var(--color-border);
            text-decoration: none;
            border-radius: var(--radius-sm);
            font-size: 0.9rem;
            transition: all 0.2s ease;
            white-space: nowrap;
            cursor: pointer;
            width: 160px;
            text-align: center;
            display: inline-block;
            box-sizing: border-box;
            height: 40px;
            line-height: 18px;
        }}
        .archive-btn:hover {{
            border-color: var(--color-primary);
            color: var(--color-primary);
        }}
        .site-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--color-primary);
            margin: 0;
        }}
        .site-subtitle {{
            font-size: 0.85rem;
            color: var(--color-text-light);
            margin: 0;
        }}
        .ai-tip {{
            background: linear-gradient(135deg, #e8f4f8, #f0f8ff);
            border: 1px solid var(--color-ai);
            border-radius: var(--radius-md);
            padding: 16px 20px;
            margin-bottom: 24px;
            position: relative;
        }}
        .ai-tip::before {{
            content: "🤖 AI学习助手";
            position: absolute;
            top: -10px;
            left: 16px;
            background: var(--color-ai);
            color: white;
            padding: 2px 10px;
            border-radius: 10px;
            font-size: 0.75rem;
        }}
        .ai-tip-content {{ margin-top: 8px; color: var(--color-secondary); }}
        .progress-section {{ margin-bottom: 32px; }}
        .progress-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 0.9rem;
            color: var(--color-text-light);
        }}
        .progress-bar {{
            height: 8px;
            background: var(--color-border);
            border-radius: 4px;
            overflow: hidden;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--color-primary), var(--color-accent));
            border-radius: 4px;
        }}
        .question-card {{
            background: var(--color-surface);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-md);
            overflow: hidden;
            margin-bottom: 32px;
        }}
        .card-header {{
            background: linear-gradient(135deg, var(--color-primary), var(--color-primary-light));
            color: white;
            padding: 24px 28px;
        }}
        .module-badge {{
            display: inline-block;
            padding: 4px 12px;
            background: rgba(255,255,255,0.2);
            border-radius: 20px;
            font-size: 0.85rem;
            margin-bottom: 12px;
        }}
        .module-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        .module-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            font-size: 0.9rem;
            opacity: 0.9;
        }}
        .meta-item {{ display: flex; align-items: center; gap: 6px; }}
        .card-body {{ padding: 28px; }}
        .question-section {{ margin-bottom: 28px; }}
        .section-label {{
            font-size: 0.85rem;
            color: var(--color-accent);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 12px;
            font-weight: 500;
        }}
        .question-text {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.25rem;
            line-height: 1.9;
            color: var(--color-secondary);
            padding: 20px;
            background: var(--color-background);
            border-radius: var(--radius-md);
            border-left: 4px solid var(--color-primary);
        }}
        .deeper-question {{
            background: #fff8e1;
            border-left-color: var(--color-accent);
            margin-top: 16px;
            font-size: 1.1rem;
        }}
        .concepts-section {{ margin-bottom: 28px; }}
        .concepts-grid {{ display: flex; flex-wrap: wrap; gap: 10px; }}
        .concept-tag {{
            padding: 8px 16px;
            background: var(--color-background);
            border: 1px solid var(--color-border);
            border-radius: 20px;
            font-size: 0.9rem;
            color: var(--color-secondary);
            transition: all 0.2s ease;
        }}
        .concept-tag:hover {{
            background: var(--color-primary);
            color: white;
            border-color: var(--color-primary);
        }}
        .prompt-section {{
            background: #F5F5F0;
            border-radius: var(--radius-md);
            padding: 24px;
            margin-bottom: 28px;
        }}
        .prompt-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }}
        .prompt-title {{ font-weight: 600; color: var(--color-secondary); }}
        .copy-btn {{
            padding: 8px 16px;
            background: var(--color-primary);
            color: white;
            border: none;
            border-radius: var(--radius-sm);
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }}
        .copy-btn:hover {{ background: var(--color-primary-light); }}
        .copy-btn.copied {{ background: #2E7D32; }}
        .prompt-content {{
            font-family: 'Noto Sans SC', monospace;
            font-size: 0.9rem;
            line-height: 1.8;
            white-space: pre-wrap;
            color: var(--color-text);
            background: white;
            padding: 20px;
            border-radius: var(--radius-sm);
            border: 1px solid var(--color-border);
            max-height: 300px;
            overflow-y: auto;
        }}
        .prompt-textarea {{
            width: 100%;
            min-height: 100px;
            padding: 12px;
            font-family: 'Noto Sans SC', sans-serif;
            font-size: 0.9rem;
            line-height: 1.6;
            color: var(--color-text);
            background: #fffef8;
            border: 2px solid var(--color-accent);
            border-radius: var(--radius-sm);
            resize: vertical;
            margin: 8px 0;
            box-sizing: border-box;
        }}
        .prompt-textarea:focus {{
            outline: none;
            border-color: var(--color-primary);
            box-shadow: 0 0 0 3px rgba(139, 69, 19, 0.1);
        }}
        .prompt-static {{
            margin: 8px 0;
        }}
        .resources-section {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }}
        .resource-link {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 16px 20px;
            background: var(--color-background);
            border: 1px solid var(--color-border);
            border-radius: var(--radius-md);
            text-decoration: none;
            color: var(--color-text);
            transition: all 0.2s ease;
        }}
        .resource-link:hover {{
            border-color: var(--color-primary);
            box-shadow: var(--shadow-sm);
            transform: translateY(-2px);
        }}
        .resource-icon {{ font-size: 1.5rem; }}
        .resource-info {{ flex: 1; }}
        .resource-title {{ font-weight: 500; margin-bottom: 2px; }}
        .resource-detail {{ font-size: 0.85rem; color: var(--color-text-light); }}
        .archive-section {{
            background: var(--color-surface);
            border-radius: var(--radius-lg);
            padding: 24px 28px;
            box-shadow: var(--shadow-sm);
        }}
        .archive-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .archive-title {{ font-weight: 600; color: var(--color-secondary); }}
        .archive-select {{
            padding: 10px 20px;
            border: 1px solid var(--color-border);
            border-radius: var(--radius-sm);
            background: white;
            font-size: 0.9rem;
            cursor: pointer;
            width: 200px;
            height: 40px;
            transition: all 0.2s ease;
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23666' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 12px center;
            padding-right: 32px;
            box-sizing: border-box;
            line-height: 18px;
        }}
        .archive-select:hover {{
            border-color: var(--color-primary);
        }}
        footer {{
            text-align: center;
            padding-top: 32px;
            color: var(--color-text-light);
            font-size: 0.85rem;
        }}
        footer a {{ color: var(--color-primary); text-decoration: none; }}
        footer a:hover {{ text-decoration: underline; }}
        .powered-by {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            margin-top: 8px;
            padding: 4px 12px;
            background: var(--color-ai);
            color: white;
            border-radius: 12px;
            font-size: 0.75rem;
        }}
        @media (max-width: 600px) {{
            .container {{ padding: 16px 16px 32px; }}
            header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 16px;
            }}
            .header-nav {{
                width: 100%;
                justify-content: flex-end;
            }}
            .site-title {{ font-size: 1.6rem; }}
            .module-title {{ font-size: 1.25rem; }}
            .question-text {{ font-size: 1.1rem; padding: 16px; }}
            .card-header, .card-body {{ padding: 20px; }}
            .module-meta {{ flex-direction: column; gap: 8px; }}
            .archive-select {{ width: 180px; }}
            .archive-btn {{ width: 120px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="header-left">
                <h1 class="site-title">天纪每日学习</h1>
                <p class="site-subtitle">倪海厦天纪课程 · 费曼学习法 · Claude AI增强</p>
            </div>
            <div class="header-nav">
                <a href="archive/index.html" class="archive-btn">📚 历史记录</a>
                <select class="archive-select" onchange="goToArchive(this.value)">
                    <option value="">📅 {today_display}</option>
                    {archive_options}
                </select>
            </div>
        </header>

        <div class="ai-tip">
            <div class="ai-tip-content">
                <strong>今日学习提示：</strong>{enhanced_content.get('daily_tip', '认真观看视频，做好笔记。')}
                <br><br>
                <strong>知识关联：</strong>{enhanced_content.get('connection_hint', '思考本模块与整体体系的关系。')}
            </div>
        </div>

        <div class="progress-section">
            <div class="progress-header">
                <span>学习进度</span>
                <span>第 {current_num} / {total_num} 模块</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress_percent}%"></div>
            </div>
        </div>

        <div class="question-card">
            <div class="card-header">
                <div class="module-badge">模块 {module['id']}</div>
                <h2 class="module-title">{module['title']}</h2>
                <div class="module-meta">
                    <span class="meta-item"><span>📺</span><span>第 {module['episode']} 集</span></span>
                    <span class="meta-item"><span>📖</span><span>教材第 {module['textbook_pages']} 页</span></span>
                </div>
            </div>

            <div class="card-body">
                <div class="question-section">
                    <div class="section-label">今日学习问题</div>
                    <div class="question-text">{module['question']}</div>
                    <div class="question-text deeper-question">
                        <strong>深入思考：</strong>{enhanced_content.get('deeper_question', module['question'])}
                    </div>
                </div>

                <div class="concepts-section">
                    <div class="section-label">核心概念</div>
                    <div class="concepts-grid">
                        {concepts_html}
                    </div>
                </div>

                <div class="prompt-section">
                    <div class="prompt-header">
                        <span class="prompt-title">教回提示词 (Feynman Technique)</span>
                        <button class="copy-btn" onclick="copyPrompt()">复制提示词</button>
                    </div>
                    <div class="prompt-content" id="prompt-container">{prompt_html}</div>
                </div>

                <div class="resources-section">
                    <a href="{module['video_url']}" target="_blank" rel="noopener" class="resource-link">
                        <span class="resource-icon">🎬</span>
                        <div class="resource-info">
                            <div class="resource-title">观看视频</div>
                            <div class="resource-detail">天纪第 {module['episode']} 集</div>
                        </div>
                    </a>
                    <a href="天机道教材.pdf" target="_blank" rel="noopener" class="resource-link">
                        <span class="resource-icon">📚</span>
                        <div class="resource-info">
                            <div class="resource-title">阅读教材</div>
                            <div class="resource-detail">天机道 第 {module['textbook_pages']} 页</div>
                        </div>
                    </a>
                </div>
            </div>
        </div>

        <footer>
            <p>基于费曼学习法设计 · 生成于 {generation_time}</p>
            <div class="powered-by">🤖 Powered by Claude Agent SDK</div>
        </footer>
    </div>

    <script>
        function copyPrompt() {{
            // Collect all content from the prompt container
            const container = document.getElementById('prompt-container');
            const staticDivs = container.querySelectorAll('.prompt-static');
            const textareas = container.querySelectorAll('.prompt-textarea');

            // Build the complete prompt text
            let promptText = '';
            const allElements = Array.from(container.children);

            allElements.forEach(element => {{
                if (element.classList.contains('prompt-static')) {{
                    promptText += element.textContent;
                }} else if (element.classList.contains('prompt-textarea')) {{
                    const userInput = element.value.trim();
                    if (userInput) {{
                        promptText += userInput;
                    }} else {{
                        promptText += '[' + element.placeholder + ']';
                    }}
                }}
            }});

            // Copy to clipboard
            navigator.clipboard.writeText(promptText).then(() => {{
                const btn = document.querySelector('.copy-btn');
                btn.textContent = '已复制!';
                btn.classList.add('copied');
                setTimeout(() => {{
                    btn.textContent = '复制提示词';
                    btn.classList.remove('copied');
                }}, 2000);
            }}).catch(() => {{
                const textarea = document.createElement('textarea');
                textarea.value = promptText;
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                const btn = document.querySelector('.copy-btn');
                btn.textContent = '已复制!';
                btn.classList.add('copied');
                setTimeout(() => {{
                    btn.textContent = '复制提示词';
                    btn.classList.remove('copied');
                }}, 2000);
            }});
        }}
        function goToArchive(url) {{
            if (url) window.location.href = url;
        }}
    </script>
</body>
</html>'''

    return html


def save_html(html_content, output_path):
    """Save HTML content to file."""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated: {output_path}")


def archive_today(html_content, archive_path=ARCHIVE_PATH):
    """Save today's question to archive."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    archive_file = Path(archive_path) / f"{today_str}.html"
    archive_file.parent.mkdir(parents=True, exist_ok=True)
    with open(archive_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Archived: {archive_file}")


def generate_archive_index(modules, archive_path=ARCHIVE_PATH):
    """Generate an index page showing all archived daily questions."""
    archive_dir = Path(archive_path)
    if not archive_dir.exists():
        return

    # Get all archived files with their metadata
    archive_entries = []
    for file in sorted(archive_dir.glob("*.html"), reverse=True):
        date_str = file.stem
        try:
            date_obj = datetime.fromisoformat(date_str)

            # Calculate which module was shown on that date
            start = datetime.fromisoformat(os.getenv("START_DATE", "2026-01-21"))
            days_elapsed = (date_obj - start).days
            if days_elapsed < 0:
                days_elapsed = 0
            module_index = days_elapsed % len(modules)
            module = modules[module_index]

            archive_entries.append({
                "date": date_str,
                "date_display": date_obj.strftime("%Y年%m月%d日"),
                "weekday": date_obj.strftime("%A"),
                "module_id": module['id'],
                "module_title": module['title'],
                "episode": module['episode'],
                "url": f"{date_str}.html"
            })
        except ValueError:
            continue

    # Build archive entries HTML
    entries_html = ""
    for entry in archive_entries:
        entries_html += f'''
        <div class="archive-card">
            <div class="archive-date">
                <div class="date-large">{entry['date_display']}</div>
                <div class="date-small">{entry['weekday']}</div>
            </div>
            <div class="archive-content">
                <div class="module-badge">模块 {entry['module_id']}</div>
                <h3 class="archive-title">{entry['module_title']}</h3>
                <div class="archive-meta">第 {entry['episode']} 集</div>
            </div>
            <a href="{entry['url']}" class="archive-link">查看详情 →</a>
        </div>
        '''

    # Generate index HTML
    index_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>天纪学习历史记录 - 所有学习内容</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Noto+Sans+SC:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --color-primary: #8B4513;
            --color-primary-light: #A0522D;
            --color-secondary: #2F4F4F;
            --color-accent: #CD853F;
            --color-background: #FDF5E6;
            --color-surface: #FFFAF0;
            --color-text: #333333;
            --color-text-light: #666666;
            --color-border: #DEB887;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.08);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.1);
            --radius-md: 12px;
            --radius-lg: 16px;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 16px;
            line-height: 1.8;
            color: var(--color-text);
            background-color: var(--color-background);
            min-height: 100vh;
        }}
        .container {{ max-width: 1000px; margin: 0 auto; padding: 24px 20px 48px; }}
        header {{
            text-align: center;
            margin-bottom: 32px;
            padding-bottom: 24px;
            border-bottom: 2px solid var(--color-border);
        }}
        .site-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 2rem;
            font-weight: 700;
            color: var(--color-primary);
            margin-bottom: 8px;
        }}
        .site-subtitle {{ font-size: 0.95rem; color: var(--color-text-light); margin-bottom: 16px; }}
        .back-link {{
            display: inline-block;
            padding: 8px 16px;
            background: var(--color-primary);
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }}
        .back-link:hover {{ background: var(--color-primary-light); }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 32px;
            margin-bottom: 32px;
            padding: 20px;
            background: var(--color-surface);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-sm);
        }}
        .stat-item {{ text-align: center; }}
        .stat-number {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--color-primary);
            font-family: 'Noto Serif SC', serif;
        }}
        .stat-label {{ font-size: 0.9rem; color: var(--color-text-light); margin-top: 4px; }}
        .archive-grid {{ display: grid; gap: 20px; }}
        .archive-card {{
            display: grid;
            grid-template-columns: auto 1fr auto;
            gap: 20px;
            align-items: center;
            padding: 20px 24px;
            background: var(--color-surface);
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-sm);
            transition: all 0.2s ease;
        }}
        .archive-card:hover {{
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
        }}
        .archive-date {{ text-align: center; min-width: 120px; }}
        .date-large {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--color-primary);
            margin-bottom: 4px;
        }}
        .date-small {{ font-size: 0.85rem; color: var(--color-text-light); }}
        .archive-content {{ flex: 1; }}
        .module-badge {{
            display: inline-block;
            padding: 2px 10px;
            background: var(--color-accent);
            color: white;
            border-radius: 12px;
            font-size: 0.75rem;
            margin-bottom: 8px;
        }}
        .archive-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--color-secondary);
            margin-bottom: 4px;
        }}
        .archive-meta {{ font-size: 0.9rem; color: var(--color-text-light); }}
        .archive-link {{
            padding: 8px 16px;
            background: var(--color-primary);
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-size: 0.9rem;
            white-space: nowrap;
            transition: all 0.2s ease;
        }}
        .archive-link:hover {{ background: var(--color-primary-light); }}
        footer {{
            text-align: center;
            padding-top: 32px;
            margin-top: 32px;
            color: var(--color-text-light);
            font-size: 0.85rem;
            border-top: 1px solid var(--color-border);
        }}
        @media (max-width: 768px) {{
            .archive-card {{
                grid-template-columns: 1fr;
                gap: 12px;
            }}
            .archive-date {{ text-align: left; }}
            .stats {{ flex-direction: column; gap: 16px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1 class="site-title">天纪学习历史记录</h1>
            <p class="site-subtitle">所有每日学习内容汇总</p>
            <a href="../index.html" class="back-link">← 返回今日学习</a>
        </header>

        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">{len(archive_entries)}</div>
                <div class="stat-label">学习天数</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{len(modules)}</div>
                <div class="stat-label">学习模块</div>
            </div>
        </div>

        <div class="archive-grid">
            {entries_html}
        </div>

        <footer>
            <p>天纪每日学习系统 · 基于费曼学习法设计</p>
            <p style="margin-top: 8px;">🤖 Powered by Claude Agent SDK</p>
        </footer>
    </div>
</body>
</html>'''

    # Save index file
    index_file = archive_dir / "index.html"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_html)
    print(f"Generated archive index: {index_file}")


async def main():
    """Main function using Claude Agent SDK."""
    print("=" * 50)
    print("天纪学习系统 - Claude Agent SDK 版本")
    print("=" * 50)

    # Load modules
    print("\n正在加载学习模块...")
    data = load_modules()
    modules = data['modules']
    print(f"已加载 {len(modules)} 个学习模块")

    # Calculate today's module
    today_str = datetime.now().strftime("%Y-%m-%d")
    module, current_num, total_num = calculate_daily_module(modules)
    print(f"\n今日模块: {module['title']} (第 {current_num}/{total_num} 个)")

    # Generate enhanced content with Claude
    print("\n正在使用 Claude AI 生成增强内容...")
    enhanced_content = await generate_enhanced_content(module, current_num, total_num)
    print("AI增强内容生成完成")

    # Get archived dates for main page (with archive/ prefix)
    archived_dates_main = get_archived_dates(is_archive_page=False)
    print(f"已找到 {len(archived_dates_main)} 个历史记录")

    # Generate HTML for main page
    print("\n正在生成HTML页面...")
    html_content_main = generate_html(
        module=module,
        current_num=current_num,
        total_num=total_num,
        archived_dates=archived_dates_main,
        today_date=today_str,
        enhanced_content=enhanced_content
    )

    # Save main page
    save_html(html_content_main, OUTPUT_PATH)

    # Get archived dates for archive page (without archive/ prefix)
    archived_dates_archive = get_archived_dates(is_archive_page=True)

    # Generate HTML for archive page with corrected URLs
    html_content_archive = generate_html(
        module=module,
        current_num=current_num,
        total_num=total_num,
        archived_dates=archived_dates_archive,
        today_date=today_str,
        enhanced_content=enhanced_content
    )

    # Archive today's question with corrected URLs
    archive_today(html_content_archive)

    # Generate archive index page
    print("\n正在生成历史记录索引页面...")
    generate_archive_index(modules)

    print("\n" + "=" * 50)
    print("生成完成！(Powered by Claude Agent SDK)")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
