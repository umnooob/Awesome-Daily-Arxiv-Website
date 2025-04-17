# Daily arXiv Papers with AI Enhancement

This project automatically crawls arXiv papers daily and uses AI to generate summaries. The results are presented in a modern web interface that allows you to browse and search papers by category.

[中文版](./README.zh.md)

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
