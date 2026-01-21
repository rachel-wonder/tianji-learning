# 天纪学习系统 - 详细实施计划
# Tianji Learning System - Detailed Implementation Plan

---

## 目录 (Table of Contents)

1. [项目概述](#1-项目概述)
2. [前置准备](#2-前置准备)
3. [Phase 1: API密钥获取](#phase-1-api密钥获取)
4. [Phase 2: 代码审查与定制](#phase-2-代码审查与定制)
5. [Phase 3: GitHub仓库创建](#phase-3-github仓库创建)
6. [Phase 4: Secrets配置](#phase-4-secrets配置)
7. [Phase 5: 代码推送](#phase-5-代码推送)
8. [Phase 6: GitHub Pages启用](#phase-6-github-pages启用)
9. [Phase 7: 工作流测试](#phase-7-工作流测试)
10. [Phase 8: 验证与监控](#phase-8-验证与监控)
11. [后续维护](#后续维护)
12. [故障排除](#故障排除)

---

## 1. 项目概述

### 1.1 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions (每日触发)                  │
│                         ↓                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              generate_question.py                     │   │
│  │  ┌─────────────┐    ┌─────────────┐                 │   │
│  │  │ modules.json │ → │ Claude SDK  │ → AI增强内容     │   │
│  │  └─────────────┘    └─────────────┘                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                         ↓                                    │
│              生成 HTML → docs/index.html                     │
│                         ↓                                    │
│              GitHub Pages 自动部署                           │
│                         ↓                                    │
│              用户访问学习页面                                 │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 核心文件清单

| 文件路径 | 功能 | 需要修改 |
|---------|------|---------|
| `src/modules.json` | 学习模块数据库 | ✅ 需更新视频URL |
| `src/generate_question.py` | 主生成脚本(Claude SDK) | ⬜ 可选 |
| `.github/workflows/daily-question.yml` | GitHub Actions工作流 | ⬜ 可选 |
| `docs/index.html` | 生成的学习页面 | 🔄 自动生成 |
| `requirements.txt` | Python依赖 | ⬜ 无需修改 |

### 1.3 所需账号和服务

| 服务 | 用途 | 费用 |
|------|------|------|
| GitHub账号 | 代码托管、Actions、Pages | 免费 |
| Anthropic账号 | Claude API调用 | 按量付费 |

---

## 2. 前置准备

### 2.1 环境检查清单

```bash
# 检查 Git 是否安装
git --version
# 期望输出: git version 2.x.x

# 检查 GitHub CLI (可选但推荐)
gh --version
# 如未安装: brew install gh (macOS)
```

### 2.2 本地项目文件确认

```bash
# 确认项目目录结构
ls -la /Users/qiu/Documents/黄叔编程/tianji-learning/

# 期望看到:
# .github/
# docs/
# src/
# templates/
# requirements.txt
# README.md
```

### 2.3 预估成本

| 项目 | 成本 |
|------|------|
| GitHub (仓库/Actions/Pages) | $0 (免费) |
| Anthropic Claude API | ~$0.01-0.05/次生成 |
| 每月预估 (每日运行) | ~$0.30-1.50/月 |

---

## Phase 1: API密钥获取

### 1.1 创建Anthropic账号

**步骤:**

1. 访问 https://console.anthropic.com/
2. 点击 **Sign Up** 或 **Get Started**
3. 使用邮箱注册或Google账号登录
4. 完成邮箱验证

### 1.2 设置付款方式

**步骤:**

1. 登录后进入 **Settings** → **Billing**
2. 添加信用卡或其他付款方式
3. 设置消费限额 (建议: $5-10/月)

### 1.3 生成API密钥

**步骤:**

1. 进入 **API Keys** 页面
   ```
   https://console.anthropic.com/settings/keys
   ```

2. 点击 **Create Key**

3. 设置名称: `tianji-learning-github-actions`

4. 复制密钥 (格式: `sk-ant-api03-...`)

5. **立即保存到安全位置** - 密钥只显示一次!

### 1.4 验证密钥 (可选)

```bash
# 在终端测试密钥是否有效
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: YOUR_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

---

## Phase 2: 代码审查与定制

### 2.1 更新学习模块数据

**文件:** `src/modules.json`

**必须修改:**
- `video_url`: 替换为真实的天纪视频链接

```json
{
  "id": "001",
  "title": "紫微斗数基础入门",
  "episode": "1-3",
  "video_url": "https://www.youtube.com/watch?v=REAL_VIDEO_ID",  // ← 修改这里
  "textbook_pages": "1-15",
  ...
}
```

### 2.2 可选定制项

#### A. 修改起始日期

**文件:** `src/generate_question.py` (第19行)

```python
START_DATE = os.getenv("START_DATE", "2026-01-21")  # 修改为你想要的起始日期
```

#### B. 修改定时任务时间

**文件:** `.github/workflows/daily-question.yml` (第6行)

```yaml
schedule:
  - cron: '0 8 * * *'  # UTC时间 8:00 = 北京时间 16:00
  # 修改为其他时间，例如:
  # - cron: '0 0 * * *'  # UTC 0:00 = 北京时间 8:00
```

#### C. 添加更多学习模块

在 `src/modules.json` 中添加新模块:

```json
{
  "id": "006",
  "title": "新模块标题",
  "episode": "XX-XX",
  "video_url": "https://...",
  "textbook_pages": "XX-XX",
  "question": "学习问题",
  "key_concepts": ["概念1", "概念2"],
  "prompt_template": "费曼学习法提示词..."
}
```

### 2.3 代码审查检查清单

| 检查项 | 状态 |
|--------|------|
| modules.json 格式正确 (有效JSON) | ⬜ |
| 所有video_url已替换为真实链接 | ⬜ |
| textbook_pages页码准确 | ⬜ |
| prompt_template内容完整 | ⬜ |
| 无敏感信息泄露 | ⬜ |

---

## Phase 3: GitHub仓库创建

### 3.1 方法A: 通过网页创建

**步骤:**

1. 登录 GitHub: https://github.com

2. 点击右上角 **+** → **New repository**

3. 填写信息:
   - Repository name: `tianji-learning`
   - Description: `天纪每日学习系统 - Powered by Claude AI`
   - Visibility: **Public** ⚠️ (GitHub Pages免费版需要Public)
   - **不要** 勾选 "Add a README file"
   - **不要** 选择 .gitignore 或 License

4. 点击 **Create repository**

### 3.2 方法B: 通过GitHub CLI创建

```bash
# 登录GitHub CLI (如果尚未登录)
gh auth login

# 创建仓库
gh repo create tianji-learning --public --description "天纪每日学习系统 - Powered by Claude AI"
```

### 3.3 记录仓库信息

创建后记录以下信息:

| 信息 | 值 |
|------|-----|
| 仓库URL | `https://github.com/YOUR_USERNAME/tianji-learning` |
| Git远程地址 | `https://github.com/YOUR_USERNAME/tianji-learning.git` |
| Pages URL (稍后) | `https://YOUR_USERNAME.github.io/tianji-learning` |

---

## Phase 4: Secrets配置

### 4.1 进入Secrets设置页面

```
https://github.com/YOUR_USERNAME/tianji-learning/settings/secrets/actions
```

或通过界面导航:
1. 进入仓库页面
2. 点击 **Settings** (齿轮图标)
3. 左侧菜单: **Secrets and variables** → **Actions**

### 4.2 添加ANTHROPIC_API_KEY

**步骤:**

1. 点击 **New repository secret**

2. 填写:
   - **Name:** `ANTHROPIC_API_KEY`
   - **Secret:** 粘贴你的API密钥 (`sk-ant-api03-...`)

3. 点击 **Add secret**

### 4.3 验证Secret已添加

在 **Repository secrets** 列表中应看到:

```
ANTHROPIC_API_KEY    Updated just now
```

### 4.4 Secrets配置检查清单

| Secret名称 | 状态 | 备注 |
|-----------|------|------|
| ANTHROPIC_API_KEY | ⬜ | 必须配置 |

---

## Phase 5: 代码推送

### 5.1 初始化本地Git仓库

```bash
# 进入项目目录
cd /Users/qiu/Documents/黄叔编程/tianji-learning

# 初始化Git仓库
git init

# 查看状态
git status
```

### 5.2 创建.gitignore (推荐)

```bash
# 创建.gitignore文件
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
.env
venv/
.venv/

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db

# Local testing
test_output/
*.log
EOF
```

### 5.3 添加并提交文件

```bash
# 添加所有文件
git add .

# 查看将要提交的文件
git status

# 创建初始提交
git commit -m "Initial commit: 天纪学习系统 with Claude Agent SDK

Features:
- Daily learning question generation
- Claude AI enhanced content
- Feynman Technique teaching-back prompts
- GitHub Actions automation
- GitHub Pages deployment"
```

### 5.4 连接远程仓库并推送

```bash
# 添加远程仓库 (替换YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/tianji-learning.git

# 确认远程仓库
git remote -v

# 重命名分支为main
git branch -M main

# 推送到GitHub
git push -u origin main
```

### 5.5 推送检查清单

| 步骤 | 命令 | 状态 |
|------|------|------|
| 初始化仓库 | `git init` | ⬜ |
| 添加文件 | `git add .` | ⬜ |
| 提交 | `git commit -m "..."` | ⬜ |
| 添加远程 | `git remote add origin ...` | ⬜ |
| 推送 | `git push -u origin main` | ⬜ |

---

## Phase 6: GitHub Pages启用

### 6.1 进入Pages设置

```
https://github.com/YOUR_USERNAME/tianji-learning/settings/pages
```

### 6.2 配置Pages

1. **Source:** Deploy from a branch

2. **Branch:**
   - 选择: `main`
   - 文件夹: `/docs`

3. 点击 **Save**

### 6.3 等待部署

- 首次部署需要1-3分钟
- 刷新页面查看部署状态
- 成功后会显示: "Your site is live at https://..."

### 6.4 验证Pages部署

访问:
```
https://YOUR_USERNAME.github.io/tianji-learning
```

应该能看到初始的学习页面。

---

## Phase 7: 工作流测试

### 7.1 进入Actions页面

```
https://github.com/YOUR_USERNAME/tianji-learning/actions
```

### 7.2 手动触发工作流

1. 左侧选择 **Generate Daily Question (Claude Agent SDK)**

2. 点击 **Run workflow** 下拉按钮

3. 确保选择 `main` 分支

4. 点击绿色 **Run workflow** 按钮

### 7.3 监控执行过程

1. 点击正在运行的workflow查看详情

2. 展开每个步骤查看日志:
   - ✅ Checkout repository
   - ✅ Set up Python
   - ✅ Install Claude Code CLI
   - ✅ Install Python dependencies
   - ✅ Generate daily question with Claude AI
   - ✅ Configure Git
   - ✅ Commit and push changes

### 7.4 常见问题排查

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `ANTHROPIC_API_KEY not found` | Secret未配置 | 检查Phase 4 |
| `Permission denied` | 仓库权限问题 | 检查workflow permissions |
| `Claude SDK error` | API调用失败 | 检查API密钥和余额 |
| `Push failed` | 分支保护 | 检查分支设置 |

### 7.5 工作流测试检查清单

| 检查项 | 状态 |
|--------|------|
| 工作流成功运行 | ⬜ |
| Claude AI内容生成正常 | ⬜ |
| docs/index.html已更新 | ⬜ |
| 自动提交成功 | ⬜ |
| Pages页面已更新 | ⬜ |

---

## Phase 8: 验证与监控

### 8.1 功能验证清单

| 功能 | 验证方法 | 状态 |
|------|----------|------|
| 页面加载 | 访问Pages URL | ⬜ |
| 中文显示 | 检查字体渲染 | ⬜ |
| AI增强内容 | 查看"AI学习助手"区域 | ⬜ |
| 复制按钮 | 点击测试复制功能 | ⬜ |
| 视频链接 | 点击测试跳转 | ⬜ |
| 移动端响应 | 手机访问测试 | ⬜ |

### 8.2 设置执行通知 (可选)

在仓库Settings中启用通知:
1. **Settings** → **Notifications**
2. 勾选 **Actions** 相关通知

### 8.3 监控API使用量

定期检查Anthropic控制台:
```
https://console.anthropic.com/settings/usage
```

---

## 后续维护

### 日常维护任务

| 频率 | 任务 | 说明 |
|------|------|------|
| 每周 | 检查Actions运行状态 | 确保每日生成正常 |
| 每月 | 检查API账单 | 控制成本 |
| 按需 | 添加新学习模块 | 扩展内容 |
| 按需 | 更新视频链接 | 维护有效性 |

### 添加新模块流程

1. 编辑 `src/modules.json`
2. 添加新模块数据
3. 提交并推送:
   ```bash
   git add src/modules.json
   git commit -m "Add new module: 模块名称"
   git push
   ```

### 更新视频链接流程

1. 编辑 `src/modules.json`
2. 更新 `video_url` 字段
3. 提交并推送

---

## 故障排除

### 问题1: GitHub Actions失败

**症状:** 工作流显示红色X

**排查步骤:**
1. 查看失败步骤的日志
2. 检查错误信息
3. 常见原因:
   - API密钥错误/过期
   - API余额不足
   - 代码语法错误

### 问题2: Pages不更新

**症状:** 运行成功但页面未变化

**排查步骤:**
1. 检查 `docs/index.html` 是否有新提交
2. 清除浏览器缓存
3. 等待2-3分钟后刷新

### 问题3: Claude AI生成失败

**症状:** 页面显示默认内容而非AI增强内容

**排查步骤:**
1. 检查Actions日志中的Claude SDK输出
2. 确认API密钥有效
3. 确认API余额充足

### 问题4: 中文显示乱码

**症状:** 页面文字显示为方块或问号

**排查步骤:**
1. 确认HTML有 `<meta charset="UTF-8">`
2. 确认文件以UTF-8编码保存
3. 检查浏览器编码设置

---

## 实施进度追踪表

| Phase | 任务 | 开始时间 | 完成时间 | 状态 |
|-------|------|----------|----------|------|
| 1 | API密钥获取 | | | ⬜ |
| 2 | 代码审查与定制 | | | ⬜ |
| 3 | GitHub仓库创建 | | | ⬜ |
| 4 | Secrets配置 | | | ⬜ |
| 5 | 代码推送 | | | ⬜ |
| 6 | GitHub Pages启用 | | | ⬜ |
| 7 | 工作流测试 | | | ⬜ |
| 8 | 验证与监控 | | | ⬜ |

---

## 联系与支持

- **GitHub Issues:** 报告问题
- **Anthropic文档:** https://docs.anthropic.com/
- **GitHub Actions文档:** https://docs.github.com/en/actions
- **GitHub Pages文档:** https://docs.github.com/en/pages

---

*文档版本: 1.0*
*最后更新: 2026-01-21*
*作者: Claude AI Assistant*
