# 天纪每日学习系统

基于费曼学习法的自动化学习系统，每日一问，你教给你的AI。把【视频时间戳】和【教材对应内容】关联起来，知识点不迷路。

## 功能特点

- **每日学习问题**：自动轮换学习模块，每天推送一个学习问题
- **视频与教材同步**：解决"视频从不提及教材页码"的痛点
- **费曼学习法提示词**：生成教回提示词，配合 AI 进行深度学习
- **历史记录存档**：保留每日学习内容，支持间隔复习
- **自动化部署**：GitHub Actions 自动生成，GitHub Pages 免费托管

## 快速开始

### 1. Fork 本仓库

点击右上角 Fork 按钮，将本仓库复制到你的 GitHub 账号下。

### 2. 启用 GitHub Pages

1. 进入仓库 Settings → Pages
2. Source 选择 `main` 分支，文件夹选择 `/docs`
3. 点击 Save

### 3. 手动触发第一次生成

1. 进入 Actions 页面
2. 选择 "Generate Daily Question" workflow
3. 点击 "Run workflow"

### 4. 访问你的学习页面

`https://YOUR_USERNAME.github.io/tianji-learning`

## 项目结构

```
tianji-learning/
├── .github/workflows/
│   └── daily-question.yml    # GitHub Actions 工作流
├── src/
│   ├── generate_question.py  # 问题生成脚本
│   └── modules.json          # 学习模块数据
├── templates/
│   └── question.html         # HTML 模板
├── docs/                     # GitHub Pages 根目录
│   ├── index.html           # 今日问题
│   ├── archive/             # 历史记录
│   └── .nojekyll
└── README.md
```

## 自定义学习模块

编辑 `src/modules.json` 添加或修改学习模块：

```json
{
  "id": "006",
  "title": "模块标题",
  "episode": "视频集数",
  "video_url": "视频链接",
  "textbook_pages": "教材页码范围",
  "question": "学习问题",
  "key_concepts": ["概念1", "概念2", "概念3"],
  "prompt_template": "费曼学习法提示词模板"
}
```

## 使用费曼学习法

1. **观看视频**：观看对应集数的天纪视频
2. **阅读教材**：阅读天机道对应页码
3. **回答问题**：用自己的话解释今日问题
4. **复制提示词**：点击"复制提示词"按钮
5. **与 AI 对话**：将提示词粘贴到 Claude/ChatGPT 等 AI 对话框
6. **教回验证**：让 AI 检验你的理解是否正确

## 技术栈

- Python 3.11+
- Jinja2 模板引擎
- GitHub Actions
- GitHub Pages

## 许可证

MIT License

## 致谢

- 倪海厦老师的天纪课程
- 费曼学习法
