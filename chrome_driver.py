from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_driver():
    options = Options()

    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-logging")
    # options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    return driver