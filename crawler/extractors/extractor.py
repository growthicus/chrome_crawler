from dataclasses import dataclass, field
from bs4 import BeautifulSoup  # type: ignore
from typing import Union, Any
from abc import ABC
from collections import defaultdict
import json


@dataclass
class Tag:
    tag: str
    all: bool = True
    attr: list[str] = field(default_factory=lambda: ["text"])


@dataclass
class Extractor(ABC):
    url: str
    result: Union[defaultdict[dict], dict] = field(
        default_factory=lambda: defaultdict(dict)
    )

    def get_tags(self) -> list[tuple[str, Any]]:
        tags = []
        for str_tag in dir(self):
            real_tag = getattr(self, str_tag)
            if isinstance(real_tag, Tag):
                tags.append((str_tag, real_tag))
        return tags

    def extract(self, soup: BeautifulSoup) -> None:
        tags = self.get_tags()
        for tag in tags:
            str_tag: str = tag[0]
            real_tag: Tag = tag[1]
            for attr in real_tag.attr:
                elems = soup.find_all(str_tag)
                self._parser(elems=elems, str_tag=str_tag, attr=attr)

        self.result["url"] = self.url
        self.result = dict(self.result)

    def _parser(self, elems: list, str_tag: str, attr: str) -> None:
        if attr == "text":
            data = [elem.text for elem in elems if elem.text != ""]
        else:
            data = [elem.get(attr) for elem in elems]

        self.result[str_tag][attr] = data

    def jsonify(self) -> str:
        return json.dumps(
            self.result,
            sort_keys=True,
            indent=4,
            separators=(",", ": "),
            ensure_ascii=False,
        )