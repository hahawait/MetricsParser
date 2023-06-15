import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def create_driver(with_caps: bool = True):
    # Отключить журналирование Selenium
    logging.disable(logging.INFO)

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"

    options = Options()

    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-logging")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument('--headless')
    if with_caps:
        driver = webdriver.Chrome(options=options, desired_capabilities=caps)
    else:
        driver = webdriver.Chrome(options=options)
    return driver