"""
Модуль для проверки подключенных метрик к сайтам
"""
from multiprocessing import Process, Queue

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC

from chrome_driver import create_driver


def process_links(links, output_queue):
    driver = create_driver()
    sources_links = []
    not_valid_links = []
    for link in links:
        try:
            driver.get(link)
            # Явное ожидание появления метрик в блоке head
            WebDriverWait(driver, 5).until(
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
    driver.quit()

    # Помещаем результаты в очередь
    output_queue.put((sources_links, not_valid_links))

def check_sources_links(links):
    """
    Метод для проверки подключенных метрик к сайтам.
    Возвращает список сайтов с подключенными метриками
    и список не валидных ссылок.
    """
    midpoint = len(links) // 2
    links_a = links[:midpoint]
    links_b = links[midpoint:]

    # Создание очереди для получения результатов
    output_queue = Queue()

    # Создание двух процессов для обработки каждой половины ссылок
    process_a = Process(target=process_links, args=(links_a, output_queue))
    process_b = Process(target=process_links, args=(links_b, output_queue))

    # Запуск процессов
    process_a.start()
    process_b.start()

    # Ожидание завершения процессов
    process_a.join()
    process_b.join()

    # Получение результатов из очереди
    sources_links = []
    not_valid_links = []

    while not output_queue.empty():
        result = output_queue.get()
        sources_links.extend(result[0])
        not_valid_links.extend(result[1])

    return sources_links, not_valid_links
