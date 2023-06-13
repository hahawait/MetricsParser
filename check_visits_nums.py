import time
from bs4 import BeautifulSoup

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
            print(f"Успешно обработана: {link}")
        except Exception as e:
            print(f"Ошибка при обработке ссылки {link}")
            visits_numbers.append('0K')
        finally:
            driver.quit()
    print('Получение количества посещений закончено.')
    return visits_numbers


def check_visits_value(base_links, visits_nums):
    filtered_links = []

    for link, visits in zip(base_links, visits_nums):
        value_str = visits[:-1]                         # Извлекаем числовое значение без символа масштаба
        scale = visits[-1]                              # Извлекаем символ масштаба

        if scale == 'M':                                # Если количество посещений больше 1млн
            filtered_links.append((link, visits))       # Добавляем пару (ссылка, значение visits_nums)
        elif scale == 'K' and float(value_str) > 6.0:   # Если количество посещений больше 6к
            filtered_links.append((link, visits))       # Добавляем пару (ссылка, значение visits_nums)

    return filtered_links


def get_valid_links(sources_links):
    print('\n\n\nЧекаем количество посещений на сайтах с подключенными метриками')
    similar_links = transform_links(sources_links)
    visits_num = get_visits_value(similar_links)
    valid_links = check_visits_value(sources_links, visits_num)
    return valid_links
