from dataclasses import dataclass, field
import tldextract
from typing import Union


@dataclass
class ServerSettings:
    host: str = "http://chrome"
    port: str = "5000"


@dataclass
class CrawlerSettings:
    start_url: Union[str, None] = None
    max_threads: int = 10
    api_timeout: int = 10
    url_not_contain: list[str] = field(default_factory=lambda: [])
    url_contain: list[str] = field(default_factory=lambda: [])
    url_tld_match: bool = True
    subdomains: bool = False

    def validate_url(self, url: str):
        org_tld = tldextract.extract(self.start_url)
        tld = tldextract.extract(url)
        if self.url_tld_match:
            if org_tld.domain != tld.domain or org_tld.suffix != tld.suffix:
                return False

        if not self.subdomains:
            if org_tld.subdomain != tld.subdomain:
                return False

        if any(p in url for p in self.url_not_contain):
            return False

        if self.url_contain:
            if not any(p in url for p in self.url_contain):
                return False

        return True
