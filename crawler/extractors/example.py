from dataclasses import dataclass
from .extractor import Extractor, Tag


@dataclass
class Data(Extractor):
    title = Tag(tag="title")
