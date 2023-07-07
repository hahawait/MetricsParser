"""
Модуль для проверки количества посещений сайта
Использует сайт https://www.similarweb.com
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _transform_link(link):
    """
    Метод преобразовывает ссылку для similarweb
    """

    if link.startswith("http://"):
        link = link.replace("http://", "https://www.similarweb.com/website/")
    elif link.startswith("https://"):
        link = link.replace("https://", "https://www.similarweb.com/website/")
    transform_link = link.rstrip('/') + "/#overview"
    return transform_link


def _get_visits_value(link, driver):
    """
    Метод определяет количество посещений сайта
    """

    transform_link = _transform_link(link)

    try:
        driver.get(transform_link)
        # Явное ожидание появления элемента с классом 'engagement-list__item-value'
        value_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'engagement-list__item-value'))
        )
        visits_number = value_element.text
        print(f"Успешно обработана: {transform_link}")
    except Exception:
        print(f"Ошибка при обработке ссылки {transform_link}")
        visits_number = None

    return visits_number


def check_visits_value(link, driver, target_nums):
    """
    Метод сравнивает количество посещений сайта с заданным значением
    """

    visits = _get_visits_value(link, driver)
    print(f'Количество посещений: {visits}\n')

    if visits is not None:
        # Извлекаем числовое значение без символа масштаба
        value_str = visits[:-1]
        # Извлекаем символ масштаба
        scale = visits[-1]
        if scale == 'M':
            return visits
        elif scale == 'K' and float(value_str) > float(target_nums):
            return visits
        else:
            print()
            return False
    else:
        return None
