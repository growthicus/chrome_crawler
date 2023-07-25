from flask import Flask, request  # type: ignore
from dataclasses import dataclass
from chrome import chrome_driver  # type: ignore

app = Flask(__name__)


@dataclass
class RenderRequest:
    url: str


def chrome_render(req: RenderRequest) -> str:
    driver = chrome_driver()
    driver.get(req.url)
    html = driver.page_source
    driver.quit()
    return html


@app.route("/render", methods=["POST"])
def render():
    req = RenderRequest(**request.json)
    html = chrome_render(req=req)
    return html
