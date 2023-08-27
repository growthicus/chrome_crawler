from dataclasses import dataclass
from .extractor import Extractor, Tag


@dataclass
class Data(Extractor):
    price = Tag(
        tag="price",
        xpath="/html/body/div[2]/div[1]/div/div[2]/div[2]/div[4]/div[1]/div[3]/main/div[1]/div/div[2]/div[2]/div/p/span",
    )
    tilte = Tag(
        tag="title",
        xpath="/html/body/div[2]/div[1]/div/div[2]/div[2]/div[4]/div[1]/div[3]/main/div[1]/div/div[2]/div[1]/h1",
    )
    desc = Tag(
        tag="desc1",
        xpath="/html/body/div[2]/div[1]/div/div[2]/div[2]/div[4]/div[1]/div[3]/main/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/p[2]",
    )
    desc = Tag(
        tag="desc2",
        xpath="/html/body/div[2]/div[1]/div/div[2]/div[2]/div[4]/div[1]/div[3]/main/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/p[3]",
    )
    desc = Tag(
        tag="desc3",
        xpath="/html/body/div[2]/div[1]/div/div[2]/div[2]/div[4]/div[1]/div[3]/main/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/p[4]",
    )
    brand = Tag(
        tag="brand",
        xpath="/html/body/div[2]/div[1]/div/div[2]/div[2]/div[4]/div[1]/div[3]/main/div[1]/div/div[2]/div[1]/div/ul/li/a",
    )
