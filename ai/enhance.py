import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict

import dotenv
from openai import OpenAI
from tqdm import tqdm

if os.path.exists(".env"):
    dotenv.load_dotenv()


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="jsonline data file")
    parser.add_argument(
        "--workers",
        type=int,
        default=3,
        help="number of worker threads",
    )
    return parser.parse_args()


def analyze_paper(
    client: OpenAI, title: str, content: str, language: str
) -> Dict[str, Any]:
    """Analyze paper content using OpenAI API"""
    system_prompt = f"""You are a professional paper analyst.
    You should not respond too long output.

    You must respond in JSON format with the following structure:
{{
    "tldr": "brief summary of the paper",
    "motivation": "what problem this paper tries to solve",
    "method": "main approach or methodology used",
    "result": "key findings or results",
    "conclusion": "main conclusions and implications"
}}
"""

    user_prompt = f"""Please analyze the following abstract of papers. 

Title:
{title}

Content:
{content}

Please generate a summary of the paper in {language}.
"""

    response = client.chat.completions.create(
        model=os.environ.get("MODEL_NAME", "deepseek-chat"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
    )

    try:
        result = json.loads(response.choices[0].message.content)
        return {
            "tldr": result.get("tldr", "Error"),
            "motivation": result.get("motivation", "Error"),
            "method": result.get("method", "Error"),
            "result": result.get("result", "Error"),
            "conclusion": result.get("conclusion", "Error"),
        }
    except json.JSONDecodeError:
        return {
            "tldr": "Error",
            "motivation": "Error",
            "method": "Error",
            "result": "Error",
            "conclusion": "Error",
        }


def process_single_paper(
    client: OpenAI, paper: Dict, language: str, output_file: str
) -> None:
    """Process a single paper and write results to file"""
    try:
        paper["AI"] = analyze_paper(client, paper["title"], paper["abstract"], language)
    except Exception as e:
        print(f"{paper['id']} has an error: {e}", file=sys.stderr)
        paper["AI"] = {
            "tldr": "Error",
            "motivation": "Error",
            "method": "Error",
            "result": "Error",
            "conclusion": "Error",
        }

    # Write results
    with open(output_file, "a") as f:
        f.write(json.dumps(paper, ensure_ascii=False) + "\n")


def main():
    args = parse_args()
    language = os.environ.get("LANGUAGE", "Chinese")

    # Initialize OpenAI client
    client = OpenAI()

    # Read and process data
    data = []
    with open(args.data, "r") as f:
        for line in f:
            data.append(json.loads(line))

    # Remove duplicates
    seen_ids = set()
    unique_data = []
    for item in data:
        if item["id"] not in seen_ids:
            seen_ids.add(item["id"])
            unique_data.append(item)

    data = unique_data
    print("Open:", args.data, file=sys.stderr)

    output_file = args.data.replace(".jsonl", f"_AI_enhanced_{language}.jsonl")

    # Process papers concurrently
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = []
        for paper in data:
            future = executor.submit(
                process_single_paper, client, paper, language, output_file
            )
            futures.append(future)

        # Show progress bar
        for _ in tqdm(
            as_completed(futures), total=len(futures), desc="Processing papers"
        ):
            pass


if __name__ == "__main__":
    main()
