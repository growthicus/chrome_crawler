from dataclasses import dataclass
from .extractor import Extractor, Tag


@dataclass
class SeoData(Extractor):
    h1 = Tag(tag="h1")
    h2 = Tag(tag="h2")
    a = Tag(tag="a", attr=["href", "text"])
