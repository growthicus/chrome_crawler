import threading
from bs4 import BeautifulSoup  # type: ignore
from urllib.parse import urljoin, urlparse
from queue import Queue, Empty
from typing import Any
import logging
import requests  # type: ignore
from settings import CrawlerSettings, ServerSettings  # type: ignore
from extractors.extractor import Extractor  # type: ignore
from functools import lru_cache
import pika  # type: ignore

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


class rabbitMQ:
    def __init__(self, server_settings: ServerSettings):
        self.server_settings = server_settings
        self.conn = self.connect()
        self.channel = self.conn.channel()

    def connect(self) -> pika.BlockingConnection:
        return pika.BlockingConnection(
            pika.ConnectionParameters(
                self.server_settings.mq_host, self.server_settings.mq_port
            )
        )

    def declare_queue(self, name: str):
        self.channel.queue_declare(queue=name)

    def send(self, channel: str, msg: str):
        self.channel.basic_publish(exchange="", routing_key=channel, body=msg)


class Crawler:
    def __init__(
        self,
        _id: str,
        start_url: str,
        crawler_settings: CrawlerSettings,
        server_settings: ServerSettings,
        extractor: Extractor,
    ):
        self._id = _id
        self.start_url = start_url
        self.extractor = extractor
        self.crawler_settings = crawler_settings
        self.server_settings = server_settings
        self.mq = rabbitMQ(server_settings=server_settings)
        self.semaphore = threading.Semaphore(crawler_settings.max_threads)
        self.urls: Queue = Queue()
        self.crawled_urls: list[str] = []

    def start(self):
        self.crawler_settings.start_url = self.start_url
        self.crawled_urls.append(self.start_url)
        self.urls.put(self.start_url)
        self.mq.declare_queue(name=self._id)
        self.start_queue()

    def start_queue(self):
        while True:
            try:
                url = self.urls.get(timeout=15)
                self.semaphore.acquire()
                self.start_thread(url)
            except Empty:
                break

            if (
                self.urls.qsize() == 0
                and self.semaphore._value == self.crawler_settings.max_threads
            ):
                break

        logging.info(
            f"Crawler stopped with {self.urls.qsize()} urls in queue and {threading.active_count()} threads active"
        )
        self.mq.conn.close()

    def start_thread(self, url: str):
        thread = CrawlThread(url=url, cls=self)
        thread.start()


class CrawlThread(threading.Thread):
    def __init__(self, url: str, cls: Crawler):
        threading.Thread.__init__(self)
        self.url: str = url
        self.cls: Crawler = cls
        self.t_extractor: Extractor = self.cls.extractor(url=url, _id=cls._id)
        self.chrome_host: str = cls.server_settings.chrome_host
        self.chrome_port: str = cls.server_settings.chrome_port

    @lru_cache(maxsize=None)
    def to_soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.render_page(), "html.parser")

    @lru_cache(maxsize=None)
    def render_page(self) -> str:
        chrome_api = f"{self.chrome_host}:{self.chrome_port}"
        r = requests.post(
            f"{chrome_api}/render",
            json={"url": self.url},
            timeout=self.cls.crawler_settings.api_timeout,
        )
        if r.status_code != 200:
            raise Exception("Failed to connect to chrome server")
        return r.text

    def process_result(self):
        self.cls.mq.send(channel=self.cls._id, msg=self.t_extractor.jsonify())

    def get_links(self) -> list[str]:
        links = [
            urljoin(self.url, link.get("href")) for link in self.to_soup().find_all("a")
        ]
        return links

    def run(self) -> None:
        self.t_extractor.extract(soup=self.to_soup())

        for url in self.get_links():
            if (
                self.cls.crawler_settings.validate_url(url=url)
                and url not in self.cls.crawled_urls
            ):
                self.cls.crawled_urls.append(url)
                self.cls.urls.put(url)

        self.render_page.cache_clear()
        self.to_soup.cache_clear()

        self.process_result()
        self.cls.semaphore.release()
