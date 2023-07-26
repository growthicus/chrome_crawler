from flask import Flask, request  # type: ignore
from dataclasses import dataclass, field
from crawler import Crawler, CrawlerSettings, ServerSettings
import json
import importlib
import threading

app = Flask(__name__)


@dataclass
class CrawlRequest:
    url: str
    crawl_id: str
    crawler_settings: dict = field(default_factory=lambda: {})
    server_settings: dict = field(default_factory=lambda: {})
    extractor: str = "example"


def crawler_start(req: CrawlRequest):
    extractor = importlib.import_module(f"extractors.{req.extractor}")

    crawler = Crawler(
        start_url=req.url,
        extractor=extractor.Data,
        crawler_settings=CrawlerSettings(**req.crawler_settings),
        server_settings=ServerSettings(**req.server_settings),
    )

    crawler.start()


@app.route("/start", methods=["POST"])
def endpoint_start():
    req = CrawlRequest(**request.json)
    t = threading.Thread(target=crawler_start, args=(req,))
    t.start()
    return request.json
