import threading
from bs4 import BeautifulSoup  # type: ignore
from urllib.parse import urljoin, urlparse
from queue import Queue
import logging
import requests  # type: ignore
from settings import CrawlerSettings, ServerSettings  # type: ignore
from extractors.extractor import Extractor  # type: ignore

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
        self.api_timeout: int = crawler_settings.api_timeout
        self.max_threads = crawler_settings.max_threads
        self.semaphore = threading.Semaphore(crawler_settings.max_threads)
        self.urls: Queue = Queue()
        self.crawled_urls: list[str] = []

    def start(self):
        self.urls.put(self.start_url)
        while True:
            url = self.urls.get()
            if (
                self.crawler_settings.validate_url(url, start_url=self.start_url)
                and url not in self.crawled_urls
            ):
                self.crawled_urls.append(url)
                self.semaphore.acquire()
                thread = CrawlThread(
                    url=url,
                    urls=self.urls,
                    semp=self.semaphore,
                    server_settings=self.server_settings,
                    extractor=self.extractor,
                )
                thread.start()

            if self.urls.qsize() == 0 and self.semaphore._value == self.max_threads:
                break


class CrawlThread(threading.Thread):
    def __init__(
        self,
        url,
        urls: Queue,
        semp: threading.Semaphore,
        server_settings: ServerSettings,
        extractor: Extractor,
    ):
        threading.Thread.__init__(self)
        self.server_settings = server_settings
        self.url = url
        self.urls = urls
        self.semp = semp
        self.html = self.render_page()
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.extractor: Extractor = extractor(url=url)

    def render_page(self) -> str:
        api_url = f"{ServerSettings.host}:{ServerSettings.port}"
        r = requests.post(f"{api_url}/render", json={"url": self.url})
        if r.status_code != 200:
            raise Exception("Failed to connect to chrome server")
        return r.text

    def get_links(self):
        links = [
            urljoin(self.url, link.get("href")) for link in self.soup.find_all("a")
        ]
        return links

    def run(self):
        # Extract data
        self.extractor.extract(soup=self.soup)
        logging.info(self.extractor.jsonify())
        # Get all links
        for url in self.get_links():
            self.urls.put(url)

        self.semp.release()
