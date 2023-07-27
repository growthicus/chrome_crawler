import threading
from bs4 import BeautifulSoup  # type: ignore
from urllib.parse import urljoin, urlparse
from queue import Queue
import logging
import requests  # type: ignore
from settings import CrawlerSettings, ServerSettings  # type: ignore
from extractors.extractor import Extractor  # type: ignore
from functools import lru_cache

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
    def __init__(self, url: str, cls: Crawler):
        threading.Thread.__init__(self)
        self.url: str = url
        self.cls: Crawler = cls
        self.t_extractor: Extractor = self.cls.extractor(url=url)
        self.chrome_host: str = cls.server_settings.chrome_host
        self.chrome_port: str = cls.server_settings.chrome_port
        self.reciever_host: str = cls.server_settings.reciever_host
        self.reciever_port: str = cls.server_settings.reciever_port

    @lru_cache(maxsize=None)
    def to_soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.render_page(), "html.parser")

    @lru_cache(maxsize=None)
    def render_page(self) -> str:
        chrome_api = f"{self.chrome_host}:{self.chrome_port}"
        r = requests.post(f"{chrome_api}/render", json={"url": self.url})
        if r.status_code != 200:
            raise Exception("Failed to connect to chrome server")
        return r.text

    def process_result(self):
        if self.reciever_host and self.reciever_port:
            reciever_api = f"{self.reciever_host}:{self.reciever_port}"
            r = requests.post(f"{reciever_api}/report", json=self.t_extractor.result)

    def get_links(self) -> list[str]:
        links = [
            urljoin(self.url, link.get("href")) for link in self.to_soup().find_all("a")
        ]
        return links

    def run(self) -> None:
        self.t_extractor.extract(soup=self.to_soup())
        self.render_page.cache_clear()
        self.to_soup.cache_clear()

        for url in self.get_links():
            if (
                self.cls.crawler_settings.validate_url(url=url)
                and url not in self.cls.crawled_urls
            ):
                self.cls.crawled_urls.append(url)
                self.cls.urls.put(url)

        self.process_result()
        self.cls.semaphore.release()
