from flask import Flask, request  # type: ignore
from dataclasses import dataclass, field
from crawler import Crawler, CrawlerSettings, ServerSettings
import importlib
import threading
import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)


@dataclass
class CrawlRequest:
    url: str
    crawl_id: str
    crawler_settings: dict = field(default_factory=lambda: {})
    server_settings: dict = field(default_factory=lambda: {})
    extractor: str = "example"


@dataclass
class StopRequest:
    crawl_id: str


def crawler_start(req: CrawlRequest):
    extractor = importlib.import_module(f"extractors.{req.extractor}")

    crawler = Crawler(
        _id=req.crawl_id,
        start_url=req.url,
        extractor=extractor.Data,
        crawler_settings=CrawlerSettings(**req.crawler_settings),
        server_settings=ServerSettings(**req.server_settings),
    )

    crawler.start()


@app.route("/start", methods=["POST"])
def endpoint_start():
    logging.info(f"crawler/start: {request.json}")
    req = CrawlRequest(**request.json)
    t = threading.Thread(target=crawler_start, args=(req,))
    t.start()
    return request.json


@app.route("/stop", methods=["POST"])
def endpoint_stop():
    logging.info(f"crawler/stop: {request.json}")
    req = StopRequest(**request.json)

    return request.json
