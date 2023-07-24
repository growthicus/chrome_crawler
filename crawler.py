import threading
from server.chrome import chrome_driver  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
from urllib.parse import urljoin, urlparse
from queue import Queue
import logging
import requests  # type: ignore

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


class Crawler:
    def __init__(self, start_url: str, max_threads: int = 10, time_out: int = 20):
        self.time_out = time_out
        self.max_threads = max_threads
        self.semaphore = threading.Semaphore(max_threads)
        self.urls: Queue = Queue()
        self.start_url = start_url
        self.netloc = urlparse(start_url).netloc
        self.crawled_urls: list = []
        self.ignore = ["#", ".pdf"]

    def rules(self, url):
        if url in self.crawled_urls:
            return False
        elif any(p in url for p in self.ignore):
            return False
        elif self.netloc != urlparse(url).netloc:
            return False

        return True

    def start(self):
        self.urls.put(self.start_url)

        while True:
            url = self.urls.get()
            if self.rules(url):
                self.crawled_urls.append(url)
                self.semaphore.acquire()
                thread = CrawlThread(url=url, urls=self.urls, semp=self.semaphore)
                thread.start()

            if self.urls.qsize() == 0 and self.semaphore._value == self.max_threads:
                break


class CrawlThread(threading.Thread):
    def __init__(self, url, urls: Queue, semp: threading.Semaphore):
        threading.Thread.__init__(self)
        self.url = url
        self.urls = urls
        self.semp = semp
        self.driver = chrome_driver()

    def render_page(self) -> str:
        r = requests.post("http://127.0.0.1:5000/render", json={"url": self.url})
        return r.text

    def get_links(self, page_source):
        soup = BeautifulSoup(self.render_page(), "html.parser")
        links = [urljoin(self.url, link.get("href")) for link in soup.find_all("a")]
        return links

    def run(self):
        logging.info(f"THREAD STARTED: {self.url}")
        # Get page source
        page_source = self.render_page()
        # Get elements
        # self.get_elements(pagesource)
        # Get all links
        for url in self.get_links(page_source):
            self.urls.put(url)

        self.semp.release()
        self.driver.quit()

        logging.info(f"THREAD ENDED: {self.url}")


#c = Crawler(start_url="https://example.com/")
#c.start()
