import threading
from bs4 import BeautifulSoup  # type: ignore
from urllib.parse import urljoin, urlparse
from queue import Queue
import logging
import requests  # type: ignore
from settings import CrawlerSettings, ServerSettings  # type: ignore
from extractors.extractor import Extractor  # type: ignore
from typing import Union
from functools import cache


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


class Crawler:
    def __init__(
        self,
        start_url: str,
        crawler_settings: CrawlerSettings,
        server_settings: ServerSettings,
        extractor: Extractor,
    ):
        self.start_url = start_url
        self.extractor = extractor
        self.crawler_settings = crawler_settings
        self.server_settings = server_settings
        self.semaphore = threading.Semaphore(crawler_settings.max_threads)
        self.urls: Queue = Queue()
        self.crawled_urls: list[str] = []

    def start(self):
        self.crawler_settings.start_url = self.start_url
        self.urls.put(self.start_url)
        while True:
            url = self.urls.get()
            self.semaphore.acquire()
            thread = CrawlThread(url=url, cls=self)
            thread.start()
            if (
                self.urls.qsize() == 0
                and self.semaphore._value == self.crawler_settings.max_threads
            ):
                break


class CrawlThread(threading.Thread):
    def __init__(self, url, cls: Crawler):
        threading.Thread.__init__(self)
        self.url: str = url
        self.cls: Crawler = cls
        self.t_extractor: Extractor = self.cls.extractor(url=url)

    @cache
    def to_soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.render_page(), "html.parser")

    @cache
    def render_page(self) -> str:
        api_url = f"{self.cls.server_settings.host}:{self.cls.server_settings.port}"
        r = requests.post(f"{api_url}/render", json={"url": self.url})
        if r.status_code != 200:
            raise Exception("Failed to connect to chrome server")
        return r.text

    def get_links(self):
        links = [
            urljoin(self.url, link.get("href")) for link in self.to_soup().find_all("a")
        ]
        return links

    def run(self):
        self.t_extractor.extract(soup=self.to_soup())
        logging.info(self.t_extractor.jsonify())
        for url in self.get_links():
            if (
                self.cls.crawler_settings.validate_url(url=url)
                and url not in self.cls.crawled_urls
            ):
                self.cls.crawled_urls.append(url)
                self.cls.urls.put(url)

        self.cls.semaphore.release()
