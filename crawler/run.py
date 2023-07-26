from crawler.crawler import Crawler
from crawler.settings import CrawerSettings, ServerSettings
import extractors

c = Crawler(
    server_settings=ServerSettings(),
    crawler_settings=CrawerSettings(
        start_url="https://www.stadium.se/sport/golf",
        url_contain=["golf"],
        extractor=extractors.OnlyTitle,
    ),
)
c.start()