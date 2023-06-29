"""
Модуль для создания и настройки драйвера
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_driver():
    """
    Создание драйвера
    """

    options = Options()

    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Отключение показа всплывающих окон и уведомлений
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")

    # Фоновый режим
    options.add_argument('--headless')

    # Отключить логи
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Отключить ожидание полной загрузки страницы
    options.page_load_strategy = 'eager'

    # Создать драйвер
    driver = webdriver.Chrome(options=options)
    return driver
