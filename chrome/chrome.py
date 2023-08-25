from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import logging
from webdriver_manager.chrome import ChromeDriverManager


def chrome_driver():
    logging.warning("Initiating Chrome!")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service("chromedriver/115.0.5790.102/chromedriver")
    return webdriver.Chrome(service=service, options=options)
