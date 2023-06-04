import time
import pandas as pd
from bs4 import BeautifulSoup
from itertools import zip_longest

from selenium.webdriver.common.by import By

from check_sources import get_source_links
from chrome_driver import create_driver


def transform_links(links):
    transformed_links = []
    for link in links:
        if link.startswith("http://"):
            link = link.replace("http://", "https://www.similarweb.com/website/")
        elif link.startswith("https://"):
            link = link.replace("https://", "https://www.similarweb.com/website/")
        link = link.rstrip('/') + "/#overview"
        transformed_links.append(link)
    return transformed_links


def get_visits_value(similar_links):
    visits_numbers = []
    for link in similar_links:
        try:
            driver = create_driver()
            driver.get(link)
            time.sleep(5)
            html = driver.page_source

            soup = BeautifulSoup(html, 'html.parser')
            # Поиск элемента с классом 'engagement-list__item-value'
            value_element = soup.find('p', class_='engagement-list__item-value')
            visits_numbers.append(value_element.text)
        except Exception as e:
            visits_numbers.append('0K')
        finally:
            driver.quit()
    return visits_numbers


def check_visits_value(base_links, visits_nums):
    filtered_links = []

    for link, visits in zip(base_links, visits_nums):
        value_str = visits[:-1]                         # Извлекаем числовое значение без символа масштаба
        scale = visits[-1]                              # Извлекаем символ масштаба

        if scale == 'M':                                # Если количество посещений больше 1млн
            filtered_links.append(link)
        elif scale == 'K' and float(value_str) > 6.0:   # Если количество посещений больше 6к
            filtered_links.append(link)

    return filtered_links


def get_valid_links(sources_links):
    similar_links = transform_links(sources_links)
    visits_numbers = get_visits_value(similar_links)
    res_list = check_visits_value(sources_links, visits_numbers)

    for i in res_list:
        print(i)
    return res_list


def save_valid_links():
    sources_links_tier_1, sources_links_tier_2 = get_source_links()
    tier1_valid_links = get_valid_links(sources_links_tier_1)
    tier2_valid_links = get_valid_links(sources_links_tier_2)
    print(f'Платные номера: {tier1_valid_links}')
    print(f'Бесплатные номера: {tier2_valid_links}')

    # Определение максимальной длины списков
    max_length = max(len(tier1_valid_links), len(tier2_valid_links))

    # Создание словаря с пустыми значениями для выравнивания длины списков
    data = {
        'Платные номера': tier1_valid_links + [''] * (max_length - len(tier1_valid_links)),
        'Бесплатные номера': tier2_valid_links + [''] * (max_length - len(tier2_valid_links))
    }
    df = pd.DataFrame(data)

    # Сохранение датафрейма в Excel
    filename = 'ссылки.xlsx'
    df.to_excel(filename, index=False)
    print(f'Ссылки сохранены в файл: {filename}')