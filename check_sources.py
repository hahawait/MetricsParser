"""
Модуль для проверки подключенных метрик к сайтам
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC


def check_sources_links(links, driver):
    """
    Метод для проверки подключенных метрик к сайтам.
    Возвращает список сайтов с подключенными метриками
    и список не валидных ссылок.
    """

    sources_links = []
    not_valid_links = []
    for link in links:
        try:
            driver.get(link)
            # Явное ожидание появления метрик в блоке head
            WebDriverWait(driver, 10).until(
                lambda driver: any(value in driver.page_source for value in ['mc.yandex.ru', 'bitrix', 'amo.crm', 'Jivo', 'calltouch'])
            )
            # Получение HTML-кода страницы
            html = driver.page_source
            # Проверка наличия требуемых значений в блоке head
            if any(value in html for value in ['mc.yandex.ru', 'bitrix', 'amo.crm', 'Jivo', 'calltouch']):
                print(f'Сайт {link} использует метрики.')
                sources_links.append(link)
            else:
                print(f'Сайт {link} НЕ использует метрики.')
        except WebDriverException:
            print(f"Ошибка при обработке ссылки {link}")
            not_valid_links.append(link)
    return sources_links, not_valid_links
