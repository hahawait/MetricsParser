"""
Модуль для проверки количества посещений сайта
Использует сайт https://www.similarweb.com
"""

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from chrome_driver import create_driver


def transform_links(links):
    """
    Метод преобразовывает ссылку для similarweb
    """

    transformed_links = []
    for link in links:
        if link.startswith("http://"):
            link = link.replace("http://", "https://www.similarweb.com/website/")
        elif link.startswith("https://"):
            link = link.replace("https://", "https://www.similarweb.com/website/")
        link = link.rstrip('/') + "/#overview"
        transformed_links.append(link)
    return transformed_links


def get_visits_value(similar_links, driver):
    """
    Метод определяет количество посещений сайта
    """

    visits_numbers = []
    driver = create_driver()
    pause_check = 0
    for link in similar_links:
        pause_check += 1
        # Для обхода блокировки
        if pause_check % 25 == 0:
            print('Обработано 25 ссылок, пауза 3 минуты...')
            driver.quit()
            time.sleep(180)
            print('Продолжаем')
            driver = create_driver()
        try:
            driver.get(link)

            # Явное ожидание появления элемента с классом 'engagement-list__item-value'
            value_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'engagement-list__item-value'))
            )

            visits_numbers.append(value_element.text)
            print(f"Успешно обработана: {link}")
        except Exception:
            print(f"Ошибка при обработке ссылки {link}")
            visits_numbers.append('0K')
    driver.quit()
    return visits_numbers


def check_visits_value(base_links, visits_nums, target_nums):
    """
    Метод сравнивает количество посещений сайта с заданным значением
    """

    filtered_links = []
    not_valid_links = []
    for link, visits in zip(base_links, visits_nums):
        value_str = visits[:-1]                         # Извлекаем числовое значение без символа масштаба
        scale = visits[-1]                              # Извлекаем символ масштаба

        if scale == 'M':                                                # Если количество посещений больше 1млн
            filtered_links.append((link, visits))                       # Добавляем пару (ссылка, значение visits_nums)
        elif scale == 'K' and float(value_str) > float(target_nums):    # Если количество посещений больше заданного числа
            filtered_links.append((link, visits))                       # Добавляем пару (ссылка, значение visits_nums)
        elif scale == 'K' and float(value_str) == 0:                    # Если количество посещений равно 0
            not_valid_links.append(link)                                # Добавляем ссылку в список not_valid_links

    return filtered_links, not_valid_links
