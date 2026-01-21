# Product Requirements Document (PRD)
# 天纪学习系统 - Tianji Learning System

**Version:** 1.0 (MVP)  
**Date:** January 20, 2026  
**Due Date:** Thursday, January 23, 2026  
**Owner:** RQ

---

## 1. Executive Summary

### Product Vision
A daily learning system that helps students master 倪海厦's 天纪 course by solving the core pain point: **videos never mention textbook page numbers**, making it impossible to synchronize video lectures with textbook reading.

### Success Criteria
- Working GitHub Pages website deployed by Thursday
- Demonstrates daily question rotation (3 modules minimum)
- Shows video-to-textbook synchronization
- Teaching-back prompt templates that work with any AI
- Classmates can immediately see the value

---

## 2. Problem Statement

### User Pain Point
**Primary User:** Students learning 天纪 from 倪海厦's YouTube videos + 天机道 textbook

**The Problem:**
- 倪海厦 NEVER mentions textbook page numbers in his 83-episode video series
- Students watch videos but don't know which textbook pages correspond
- Students read textbook but don't know which video sections to watch
- Result: Frustration, getting lost, ineffective learning

**Current Workarounds:**
- Watch entire videos repeatedly trying to find relevant sections
- Read entire textbook hoping to match content
- Ask classmates (who also don't know)
- Give up on synchronizing video + textbook

**Why This Matters:**
- Affects ALL learners using 倪海厦's materials
- No existing solution addresses this specific problem
- Proper synchronization is essential for deep learning

---

## 3. Solution Overview

### Core Innovation: Teaching-Back Learning System

**What It Does:**
1. **Daily Question:** System presents one 天纪 topic per day
2. **Study Materials:** Provides BOTH video link + textbook pages
3. **Teaching-Back:** User explains concept to AI (Feynman Technique)
4. **Universal Template:** Copy-paste prompt works with ANY AI platform

**Key Features:**
- Automated daily rotation (GitHub Actions cron)
- Historical archive (view any past day's question)
- Professional GitHub Pages website
- No login/signup required
- Works on any device

---

## 4. User Personas

### Primary: RQ (You!)
- **Background:** Learning 天纪 as preparation for Chinese medicine studies
- **Learning Style:** Gabriel Petersson's "top-down" approach (solve real problems)
- **Pain Point:** Cannot sync videos with textbook
- **Goal:** Master 天纪 fundamentals efficiently

### Secondary: Classmates
- **Background:** AI programming/Skills learning group members
- **Context:** Will see your Thursday presentation
- **Value:** Many also study 倪海厦's materials
- **Benefit:** Immediate applicability to their learning

### Tertiary: 天纪 Community
- **Background:** Thousands learning from 倪海厦's online materials
- **Pain Point:** Same video/textbook sync problem
- **Opportunity:** Open source potential, community contribution

---

## 5. User Stories

**As a 天纪 student, I want to:**
- See today's learning topic when I visit the site
- Know exactly which video episode to watch
- Know exactly which textbook pages to read
- Get a prompt template I can use with any AI
- Review previous topics via historical archive

**As a busy learner, I want to:**
- Spend 30-60 minutes per day on focused learning
- Not waste time searching for corresponding materials
- Verify my understanding through teaching-back
- Track my progress over time

---

## 6. MVP Scope (Thursday Deadline)

### In Scope ✅

**Features:**
1. **3 Learning Modules** (紫微斗数基础, 十二宫, 四化星)
2. **Daily Question Generator** (Python script)
3. **GitHub Pages Website** (HTML template)
4. **GitHub Actions Automation** (cron schedule)
5. **Historical Archive** (date selector dropdown)
6. **Teaching-Back Prompts** (copy-paste ready)

**Technical Stack:**
- Python 3.9+ (script)
- HTML/CSS/JavaScript (frontend)
- GitHub Actions (automation)
- GitHub Pages (hosting)

### Out of Scope ❌

**V1 MVP Will NOT Include:**
- User authentication/login
- Progress tracking
- Spaced repetition algorithm
- Multiple difficulty levels
- Community discussion
- Mobile app
- AI integration in website
- More than 3 modules

**V2+ Features (Post-Thursday):**
- 10-15 modules covering Episodes 1-7
- Precise video timestamps (e.g., "15:30-18:45")
- Verified textbook page numbers
- Difficulty levels
- Progress tracking
- Spaced repetition

---

## 7. Detailed Feature Specifications

### 7.1 Module Database

**Structure:**
```json
{
  "modules": [
    {
      "id": "001",
      "title": "紫微斗数三大要素",
      "episode": "2",
      "video_url": "https://www.youtube.com/watch?v=zSdakARJqhw",
      "textbook_pages": "1-10",
      "question": "紫微斗数的三大要素是什么？...",
      "key_concepts": ["天命1/3", "地理1/3", "人事1/3", "以果决行"],
      "prompt_template": "我正在学习倪海厦天纪第2集..."
    }
  ]
}
```

**Content Sources:**
- Jeff's personal notes (948 lines)
- 天机道听课笔记 (420 lines)
- 天纪紫微斗数笔记详细有图版 (1086 lines) ← Episode numbers verified

**Module 1: 紫微斗数三大要素**
- Episode 2
- Pages 1-10
- Key: 天命 + 地理 + 人事 = 完整命理

**Module 2: 十二宫与三方四正**
- Episode 2
- Pages 10-20
- Key: 命宫、财帛、官禄、迁移

**Module 3: 四化星详解**
- Episode 3
- Pages 20-35
- Key: 化科、化权、化禄、化忌

### 7.2 Daily Question Generation

**Algorithm:**
1. Calculate days since start date (e.g., Jan 1, 2026)
2. Module index = days % total_modules (rotating)
3. Load module data from JSON
4. Generate HTML page
5. Commit to repository

**Rotation Example:**
- Day 1 (Jan 1): Module 1
- Day 2 (Jan 2): Module 2
- Day 3 (Jan 3): Module 3
- Day 4 (Jan 4): Module 1 (cycles)
- ...

### 7.3 HTML Output

**Page Structure:**
```html
<!DOCTYPE html>
<html>
<head>
  <title>天纪每日一问 - [Date]</title>
  <style>/* Professional styling */</style>
</head>
<body>
  <header>
    <h1>天纪每日一问</h1>
    <p>今天是 [Date]</p>
  </header>
  
  <main>
    <section class="question">
      <h2>[Module Title]</h2>
      <p>[Learning Question]</p>
    </section>
    
    <section class="materials">
      <h3>学习材料</h3>
      <ul>
        <li>视频：<a href="[URL]">天纪第[N]集</a></li>
        <li>教材：天机道 第[X-Y]页</li>
      </ul>
    </section>
    
    <section class="key-concepts">
      <h3>重点概念</h3>
      <ul>[List of concepts]</ul>
    </section>
    
    <section class="teaching-back">
      <h3>教学反馈模板</h3>
      <textarea readonly>[Prompt template]</textarea>
      <button>复制模板</button>
    </section>
  </main>
  
  <aside class="archive">
    <h3>历史归档</h3>
    <select>[Date options]</select>
  </aside>
</body>
</html>
```

**Design Requirements:**
- Clean, professional appearance
- Mobile responsive
- Easy-to-read fonts (min 16px body text)
- Copy button for prompt template
- Clear visual hierarchy
- Matches template example aesthetic

### 7.4 GitHub Actions Workflow

**Trigger:**
```yaml
on:
  schedule:
    - cron: '0 8 * * *'  # Daily at 8am UTC
  workflow_dispatch:      # Manual trigger for testing
```

**Steps:**
1. Checkout repository
2. Set up Python 3.9
3. Run generation script
4. Commit changes (if any)
5. Push to main branch
6. GitHub Pages auto-deploys

**File Changes:**
- `index.html` (today's question)
- `archive/YYYY-MM-DD.html` (historical)
- `data/modules.json` (module database)

### 7.5 Historical Archive

**Implementation:**
- Dropdown selector with dates
- JavaScript to load archived pages
- Each day's question saved permanently
- URL structure: `/?date=2026-01-20`

**Archive Display:**
- Last 30 days in dropdown
- Link to "View All Archives"
- Preserves all generated questions

---

## 8. Technical Architecture

### 8.1 Repository Structure

```
tianji-learning/
├── .github/
│   └── workflows/
│       └── daily-question.yml
├── src/
│   ├── generate_question.py
│   └── modules.json
├── templates/
│   └── question_template.html
├── docs/  (GitHub Pages root)
│   ├── index.html
│   ├── archive/
│   │   ├── 2026-01-20.html
│   │   └── ...
│   └── styles.css
└── README.md
```

### 8.2 Data Flow

```
Cron Trigger (8am UTC)
  ↓
GitHub Actions starts
  ↓
Python script runs
  ↓
Load modules.json
  ↓
Calculate today's module
  ↓
Generate HTML from template
  ↓
Save to docs/index.html
  ↓
Archive to docs/archive/[date].html
  ↓
Git commit + push
  ↓
GitHub Pages deploys
  ↓
Users visit site
```

### 8.3 Technology Choices

**Why GitHub Actions?**
- Free for public repositories
- Reliable cron scheduling
- No server maintenance
- Matches assignment requirements

**Why GitHub Pages?**
- Free static hosting
- Automatic deployment
- Custom domain support
- Fast global CDN

**Why Python?**
- Simple templating
- JSON handling
- Date calculations
- Easy to maintain

---

## 9. Success Metrics

### MVP Success (Thursday)
- ✅ System generates daily questions
- ✅ All 3 modules work correctly
- ✅ Historical archive functions
- ✅ Site loads < 2 seconds
- ✅ Works on mobile + desktop
- ✅ Classmates understand the value

### Post-MVP Metrics (V2+)
- Daily active users
- Average time on site
- Module completion rate
- Community contributions
- GitHub stars/forks

---

## 10. User Experience Flow

### First-Time User Journey

1. **Discover:** Sees project in Thursday presentation
2. **Visit:** Goes to GitHub Pages URL
3. **Read:** Today's question about 天纪 topic
4. **Study:** Watches video + reads textbook pages
5. **Explain:** Writes understanding in own words
6. **Copy:** Copies teaching-back prompt template
7. **Verify:** Pastes into Claude/ChatGPT to verify understanding
8. **Improve:** Iterates based on AI feedback
9. **Return:** Comes back tomorrow for next topic

### Returning User Journey

1. **Visit:** Daily habit at same time
2. **Archive:** Reviews previous topics if needed
3. **Progress:** Tracks learning through module rotation
4. **Share:** Recommends to fellow 天纪 learners

---

## 11. Risks & Mitigations

### Risk 1: GitHub Actions Quota
**Risk:** Free tier has limits on actions minutes  
**Mitigation:** Script runs <1 minute/day, well within free tier  
**Backup:** Manual trigger workflow if needed

### Risk 2: Video Links Break
**Risk:** YouTube videos might be removed  
**Mitigation:** Use playlist URLs (more stable)  
**Backup:** Document episode numbers for alternate sources

### Risk 3: Textbook Pages Incorrect
**Risk:** Page estimates might not match actual content  
**Mitigation:** V1 uses "approximate" language  
**Improvement:** V2 will verify exact page numbers

### Risk 4: Low Adoption
**Risk:** Classmates might not use it  
**Mitigation:** Solve real pain point they experience  
**Strategy:** Show clear value in demo (video sync)

---

## 12. Timeline & Milestones

### Monday, Jan 20 (TODAY) ✅
- [x] Research completed
- [x] PRD finalized
- [x] 3 modules documented
- [x] Content cross-referenced

### Tuesday, Jan 21
- [ ] Write Python script (2-3 hours)
- [ ] Create HTML template (1-2 hours)
- [ ] Set up GitHub Actions (1 hour)
- [ ] Initial testing (1 hour)

### Wednesday, Jan 22
- [ ] Final testing
- [ ] Bug fixes
- [ ] Prepare demo presentation
- [ ] Create README documentation

### Thursday, Jan 23 🎯
- [ ] Present to class
- [ ] Gather feedback
- [ ] Document future improvements

---

## 13. Future Roadmap (V2+)

### Phase 2: Enhanced Content (Weeks 2-3)
- Add 7 more modules (total 10)
- Precise video timestamps
- Verified page numbers
- Difficulty levels

### Phase 3: User Features (Month 2)
- Progress tracking
- Spaced repetition
- Multiple question formats
- User notes/annotations

### Phase 4: Community (Month 3)
- Discussion forum
- User-submitted modules
- Collaborative learning
- Social sharing

### Phase 5: Advanced (Month 4+)
- Mobile app
- AI integration
- Multi-language support
- Video embedding
- Auto-generated modules

---

## 14. Dependencies

### External Dependencies
- GitHub (repository + Pages + Actions)
- YouTube (video hosting)
- User's textbook (天机道 by 倪海厦)

### Internal Dependencies
- Python 3.9+ installed locally (for development)
- Module content (COMPLETE ✅)
- Template example reference

### No Dependencies On
- User authentication services
- Database servers
- Third-party APIs
- Payment processing

---

## 15. Open Questions

### Resolved ✅
- [x] Which modules to include? → 3 modules from Episodes 2-3
- [x] How to get video-textbook mapping? → Used lecture notes
- [x] What triggers daily questions? → GitHub Actions cron
- [x] How do users teach back? → Copy-paste prompt to any AI

### Remaining ❓
- [ ] Exact hosting URL? → Will decide during implementation
- [ ] Custom domain name? → Optional, can add later
- [ ] Analytics tracking? → Maybe Google Analytics in V2

---

## 16. Appendix

### A. Module Details

See: `/mnt/user-data/outputs/FINAL_Module_Database_With_Episodes.md`

### B. Reference Materials

1. Jeff's personal notes (天纪笔记jeff个人整理.docx)
2. 天机道听课笔记.doc
3. 天纪紫微斗数笔记详细有图版.doc
4. Plus 7 additional advanced topic documents

### C. Template Example

https://backtthefuture.github.io/weibotoidea/

### D. Assignment Requirements

- Deploy Skill to GitHub Actions
- Due: Thursday, January 23, 2026
- Format: Working demo + presentation

---

## 17. Conclusion

**Ready to Build:** All research and planning COMPLETE  
**Next Step:** Implementation (Tuesday)  
**Goal:** Working MVP by Thursday  
**Impact:** Solve real pain point for 天纪 learners worldwide

---

**PRD Status:** ✅ APPROVED - Ready for Implementation  
**Last Updated:** Monday, January 20, 2026  
**Next Review:** After Thursday presentation

