from dataclasses import dataclass
from .extractor import Extractor, Tag


@dataclass
class Data(Extractor):
    price = Tag(tag="price", xpath='//*[@id="product-price"]')
    tilte = Tag(tag="title", xpath='//*[@id="product-page"]/article/div[1]/div[2]/h1')
    desc = Tag(
        tag="dec", xpath='//*[@id="product-page"]/article/div[1]/div[2]/div[4]/p'
    )
    brand = Tag(
        tag="brand",
        xpath='//*[@id="product-page"]/article/div[1]/div[2]/div[1]/a/img',
        attr=["alt"],
    )
    artnr = Tag(
        tag="artnr", xpath='//*[@id="product-page"]/article/div[1]/div[2]/div[2]/span'
    )
