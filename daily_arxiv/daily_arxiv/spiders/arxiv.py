import os

import scrapy


class ArxivSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = os.environ.get("CATEGORIES", "cs.CV")
        categories = categories.split(",")
        categories = list(map(str.strip, categories))
        self.start_urls = [
            f"https://arxiv.org/list/{cat}/new" for cat in categories
        ]  # 起始URL（计算机科学领域的最新论文）

    name = "arxiv"  # 爬虫名称
    allowed_domains = ["arxiv.org"]  # 允许爬取的域名

    def parse(self, response):
        # Extract anchor points
        anchors = []
        for li in response.css("div[id=dlpage] ul li"):
            anchors.append(int(li.css("a::attr(href)").get().split("item")[-1]))

        # Process each paper entry (dt and dd pairs)
        for paper_dt, paper_dd in zip(response.css("dl dt"), response.css("dl dd")):
            # Skip if paper is after the last anchor
            if (
                int(paper_dt.css("a[name^='item']::attr(name)").get().split("item")[-1])
                >= anchors[-1]
            ):
                continue

            # Extract paper ID
            paper_id = (
                paper_dt.css("a[title='Abstract']::attr(href)").get().split("/")[-1]
            )
            print(paper_dd.css("p.mathjax::text").get().strip())
            # Extract metadata
            yield {
                "id": paper_id,
                "title": paper_dd.css("div.list-title::text").getall()[-1].strip(),
                "authors": paper_dd.css("div.list-authors a::text").getall(),
                "abstract": paper_dd.css("p.mathjax::text").get().strip(),
                "subjects": paper_dd.css(
                    "div.list-subjects span.primary-subject::text"
                ).get()
                + paper_dd.css("div.list-subjects::text").getall()[-1].strip(),
                "comments": (
                    paper_dd.css("div.list-comments::text").getall()[-1].strip()
                    if paper_dd.css("div.list-comments")
                    else None
                ),
                "pdf_url": f"https://arxiv.org/pdf/{paper_id}.pdf",
                "abstract_url": f"https://arxiv.org/abs/{paper_id}",
            }
