#!/bin/bash

# Set default values for environment variables
export CATEGORIES=${CATEGORIES:-"cs.CV,cs.CL,cs.AI"}
export KEYWORDS=${KEYWORDS:-"Agent,Agentic,@RAG"}
export LANGUAGE=${LANGUAGE:-"Chinese"}
export MODEL_NAME=${MODEL_NAME:-"deepseek-chat"}

# Get current date
today=`date -u "+%Y-%m-%d"`

# Create data directory if it doesn't exist
mkdir -p data

# Run the crawler
echo "Running arXiv crawler..."
cd daily_arxiv
scrapy crawl arxiv -O ../data/${today}.jsonl

# Run AI enhancement
echo "Running AI enhancement..."
cd ../ai
python enhance.py --data ../data/${today}.jsonl

# Generate dates.json
echo "Generating dates.json..."
cd ..
python generate_dates.py

# For local debugging
if [ "$1" == "--debug" ]; then
    echo "Starting local server for debugging..."
    python -m http.server 8000
fi
