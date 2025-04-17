import json
import os
from glob import glob

language = os.environ.get("LANGUAGE", "Chinese")


def generate_dates_json():
    # Get all JSONL files in the data directory
    files = glob(f"data/*_AI_enhanced_{language}.jsonl")

    # Extract dates from filenames
    dates = [os.path.basename(f).split("_")[0] for f in files]

    # Sort dates in descending order
    dates.sort(reverse=True)

    # Save to dates.json
    with open("dates.json", "w") as f:
        json.dump(dates, f, indent=2)


if __name__ == "__main__":
    generate_dates_json()
