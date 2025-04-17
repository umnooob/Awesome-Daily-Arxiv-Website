import argparse
import json
import os
import sys
from typing import Any, Dict

import dotenv
from openai import OpenAI

if os.path.exists(".env"):
    dotenv.load_dotenv()


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="jsonline data file")
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

    # Process each paper
    for idx, d in enumerate(data):
        try:
            d["AI"] = analyze_paper(client, d["title"], d["abstract"], language)
        except Exception as e:
            print(f"{d['id']} has an error: {e}", file=sys.stderr)
            d["AI"] = {
                "tldr": "Error",
                "motivation": "Error",
                "method": "Error",
                "result": "Error",
                "conclusion": "Error",
            }

        # Write results
        with open(
            args.data.replace(".jsonl", f"_AI_enhanced_{language}.jsonl"), "a"
        ) as f:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")

        print(f"Finished {idx+1}/{len(data)}", file=sys.stderr)


if __name__ == "__main__":
    main()
