from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def chrome_driver():
    options = Options()
    options.add_argument("--headless")
    # options.add_argument("--no-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)
