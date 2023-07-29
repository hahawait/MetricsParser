"""
Модуль для проверки подключенных метрик к сайтам
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException


def check_sources_link(link, driver):
    """
    Метод для проверки подключенных метрик к сайтам.
    Возвращает список сайтов с подключенными метриками
    и список не валидных ссылок.
    """

    try:
        driver.get(link)
        # Явное ожидание появления метрик в блоке head
        WebDriverWait(driver, 5).until(
            lambda driver: any(value in driver.page_source for value in ['mc.yandex.ru',
                                                                         'bitrix',
                                                                         'amo.crm',
                                                                         'Jivo',
                                                                         'calltouch'])
        )
        # Получение HTML-кода страницы
        html = driver.page_source
        # Проверка наличия требуемых значений в блоке head
        if any(value in html for value in ['mc.yandex.ru',
                                           'bitrix',
                                           'amo.crm',
                                           'Jivo',
                                           'calltouch']):
            print(f'Сайт {link} использует метрики.')
            return True
        else:
            print(f'Сайт {link} НЕ использует метрики.\n\n')
            return None
    except WebDriverException:
        print(f"Ошибка при обработке ссылки {link}\n\n")
        return False
