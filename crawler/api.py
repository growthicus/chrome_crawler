from flask import Flask, request  # type: ignore
from dataclasses import dataclass, asdict
import threading
from extractors import Extractor  # type: ignore
import json

app = Flask(__name__)


@dataclass
class CrawlRequest:
    url: str
    crawl_id: str


def start_crawler(req: CrawlRequest) -> str:
    return json.dumps(asdict(req))


@app.route("/start", methods=["POST"])
def render():
    req = CrawlRequest(**request.json)
    req_json = start_crawler(req=req)
    return req_json
