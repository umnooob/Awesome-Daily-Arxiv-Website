# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import os

# useful for handling different item types with a single interface
import arxiv
from scrapy.exceptions import DropItem


class DailyArxivPipeline:
    def __init__(self):
        self.page_size = 100
        self.client = arxiv.Client(self.page_size)
        # Parse keywords and handle case sensitivity
        raw_keywords = os.environ.get("KEYWORDS", "").split(",")
        self.keywords = []
        for k in raw_keywords:
            k = k.strip()
            if k:
                # If keyword starts with @, keep original case, otherwise convert to lower
                if k.startswith("@"):
                    self.keywords.append((k[1:], True))  # (keyword, case_sensitive)
                else:
                    self.keywords.append((k.lower(), False))
        self.existing_ids = set()

    def process_item(self, item: dict, spider):
        if item["id"] in self.existing_ids:
            raise DropItem(f"Duplicate item found: {item['id']}")
        self.existing_ids.add(item["id"])

        item["authors"] = item["authors"]
        item["title"] = item["title"]
        item["categories"] = [s.strip() for s in item["subjects"].split(";")]

        if self.keywords:
            content = f"{item['title']} {item['abstract']}"
            matching_keywords = []

            for keyword, case_sensitive in self.keywords:
                if case_sensitive:
                    # Case-sensitive match
                    if keyword in content:
                        matching_keywords.append(f"@{keyword}")
                else:
                    # Case-insensitive match
                    if keyword in content.lower():
                        matching_keywords.append(keyword)

            item["matching_keywords"] = matching_keywords
            if not matching_keywords:
                raise DropItem(f"Item filtered out by keywords: {item['id']}")

        return item
