from dataclasses import dataclass, field
import tldextract
from typing import Union


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
    reciever_host: Union[str, None] = None
    reciever_port: Union[str, None] = None


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

        if any(f in url for f in non_html_extensions):
            return False

        return True
