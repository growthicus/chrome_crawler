from dataclasses import dataclass, field
import tldextract
from typing import Union
import logging

non_html_extensions = [
    # Image files
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".svg",
    ".webp",
    ".ico",
    # Video files
    ".mp4",
    ".avi",
    ".mov",
    ".flv",
    ".wmv",
    ".webm",
    # Audio files
    ".mp3",
    ".wav",
    ".ogg",
    ".flac",
    ".m4a",
    # Document files
    ".pdf",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".xls",
    ".xlsx",
    ".odt",
    ".ods",
    ".odp",
    ".txt",
    ".rtf",
    # Archive files
    ".zip",
    ".rar",
    ".7z",
    ".tar",
    ".gz",
    ".bz2",
    # Code and script files
    ".js",
    ".css",
    ".py",
    ".rb",
    ".java",
    ".c",
    ".cpp",
    # Database files
    ".sql",
    ".db",
    ".mdb",
    # Font files
    ".ttf",
    ".otf",
    ".woff",
    ".woff2",
    # Binary and executable files
    ".exe",
    ".bin",
    ".dll",
    ".so",
    ".dmg",
    # Miscellaneous file types
    ".xml",
    ".json",
    ".csv",
    ".tsv",
    ".log",
]


@dataclass
class ServerSettings:
    chrome_host: str = "http://chrome"
    chrome_port: str = "5000"
    mq_host: str = "queue"
    mq_port: str = "5672"


@dataclass
class CrawlerSettings:
    start_url: Union[str, None] = None
    max_threads: int = 10
    api_timeout: int = 10
    follow_url_not_contain: list[str] = field(default_factory=lambda: [])
    follow_url_contain: list[str] = field(default_factory=lambda: [])
    extract_url_not_contain: list[str] = field(default_factory=lambda: [])
    extract_url_contain: list[str] = field(default_factory=lambda: [])

    url_tld_match: bool = True
    subdomains: bool = False

    def validate_url(self, url: str, task="follow"):
        # Always let first URL through
        if self.start_url == url:
            return True

        if task == "follow":
            contain = self.follow_url_contain
            not_contain = self.follow_url_not_contain
        else:
            contain = self.extract_url_contain
            not_contain = self.extract_url_not_contain

        org_tld = tldextract.extract(self.start_url)
        tld = tldextract.extract(url)
        if self.url_tld_match:
            if org_tld.domain != tld.domain or org_tld.suffix != tld.suffix:
                logging.warning(f"{url} false 1")
                return False

        # example.com == www.example.com
        # dont consider www and '' as different subdomains
        if not self.subdomains and org_tld.subdomain != tld.subdomain:
            if not org_tld.subdomain and tld.subdomain == "www":
                pass
            elif not tld.subdomain and org_tld.subdomain == "www":
                pass
            else:
                logging.warning(f"{url} false 2")
                return False

        if any(p in url for p in not_contain):
            logging.warning(f"{url} did contain {contain} - {task}")
            return False

        if contain:
            if not any(p in url for p in contain):
                logging.warning(f"{url} did not contain {contain} - {task}")
                return False

        if any(f in url for f in non_html_extensions):
            return False

        return True
