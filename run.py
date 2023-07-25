from crawler import Crawler
from settings import CrawerSettings, ServerSettings
from extractors import SeoData

c = Crawler(
    server_settings=ServerSettings(),
    crawler_settings=CrawerSettings(
        start_url="https://www.stadium.se/sport/golf",
        url_contain=["golf"],
        extractor=SeoData,
    ),
)
c.start()
