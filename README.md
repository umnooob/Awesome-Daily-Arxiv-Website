# Daily arXiv Papers with AI Enhancement

This project automatically crawls arXiv papers daily and uses AI to generate summaries. The results are presented in a modern web interface that allows you to browse and search papers by category.

## Features

- Daily automatic crawling of arXiv papers
- Keyword-based filtering
- AI-powered paper summarization
- Modern web interface with search functionality
- Category-based organization
- Local debugging support

## How to Use

### Web Interface
Visit the GitHub Pages site to view the latest papers and summaries.

### Local Development
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   export CATEGORIES="cs.CV,cs.CL"  # Categories to crawl
   export KEYWORDS="deep learning,neural network"  # Optional keywords to filter
   export LANGUAGE="Chinese"  # Language for summaries
   export MODEL_NAME="deepseek-chat"  # AI model to use
   ```
4. Run the crawler:
   ```bash
   ./run.sh
   ```
5. For local debugging:
   ```bash
   ./run.sh --debug
   ```
   This will start a local server at http://localhost:8000

### GitHub Actions
The project is set up to run automatically via GitHub Actions. To customize:

1. Go to your repository's Settings -> Secrets and variables -> Actions
2. Add the following secrets:
   - `OPENAI_API_KEY`
   - `OPENAI_BASE_URL`
3. Add the following variables:
   - `CATEGORIES`: Comma-separated list of arXiv categories
   - `KEYWORDS`: Optional comma-separated list of keywords to filter (add @ prefix for case_sensitive)
   - `LANGUAGE`: Language for summaries (e.g., "Chinese" or "English")
   - `MODEL_NAME`: AI model to use
   - `EMAIL`: Your email for git commits
   - `NAME`: Your name for git commits

## Acknowledge

- Thanks for [dw-dengwei/daily-arXiv-ai-enhanced](https://github.com/dw-dengwei/daily-arXiv-ai-enhanced)

---

# 基于AI增强的每日arXiv论文

本项目每日自动爬取arXiv论文并使用AI生成摘要。结果通过现代化的Web界面呈现，允许您按类别浏览和搜索论文。

## 功能特点

- 每日自动爬取arXiv论文
- 基于关键词的过滤
- AI驱动的论文摘要生成
- 具有搜索功能的现代Web界面
- 基于类别的组织结构
- 本地调试支持

## 使用方法

### Web界面
访问GitHub Pages站点查看最新论文和摘要。

### 本地开发
1. 克隆此仓库
2. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```
3. 设置环境变量:
   ```bash
   export CATEGORIES="cs.CV,cs.CL"  # 要爬取的类别
   export KEYWORDS="deep learning,neural network"  # 可选的过滤关键词
   export LANGUAGE="Chinese"  # 摘要语言
   export MODEL_NAME="deepseek-chat"  # 使用的AI模型
   ```
4. 运行爬虫:
   ```bash
   ./run.sh
   ```
5. 本地调试:
   ```bash
   ./run.sh --debug
   ```
   这将在http://localhost:8000启动本地服务器

### GitHub Actions
该项目设置为通过GitHub Actions自动运行。自定义设置:

1. 前往仓库的Settings -> Secrets and variables -> Actions
2. 添加以下secrets:
   - `OPENAI_API_KEY`
   - `OPENAI_BASE_URL`
3. 添加以下variables:
   - `CATEGORIES`: 逗号分隔的arXiv类别列表
   - `KEYWORDS`: 可选的逗号分隔的关键词列表（添加@前缀表示大小写敏感）
   - `LANGUAGE`: 摘要语言（例如，"Chinese"或"English"）
   - `MODEL_NAME`: 使用的AI模型
   - `EMAIL`: 用于git提交的邮箱
   - `NAME`: 用于git提交的名字

## 致谢

- 感谢[dw-dengwei/daily-arXiv-ai-enhanced](https://github.com/dw-dengwei/daily-arXiv-ai-enhanced)
