import time
import pandas as pd
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_company_links(filename):
    # Загрузка Excel-таблицы
    df = pd.read_excel(filename)

    # Удаление столбцов
    columns_to_keep = ["Наименование",
                       "Веб-сайт 1", "Телефон 1", "Телефон 2"]
    df = df[columns_to_keep]

    # Удаление дубликатов
    df = df.drop_duplicates(subset=["Наименование"])
    df = df.drop_duplicates(subset=["Веб-сайт 1"])

    # Удаление компаний у которых нет сайта
    df = df.dropna(subset=["Веб-сайт 1"])

    # Фильтрация по номерам телефонов
    condition = df["Телефон 1"].astype(str).str.startswith(
        ('8800', '8495', '8812')) | df["Телефон 2"].astype(str).str.startswith(('8800', '8495', '8812'))
    matching_df = df[condition]
    non_matching_df = df[~condition]

    # Конвертация столбцов с номерами телефонов в строки без .0
    matching_df["Телефон 1"] = matching_df["Телефон 1"].astype(
        str)
    matching_df["Телефон 2"] = matching_df["Телефон 2"].astype(
        str)
    non_matching_df["Телефон 1"] = non_matching_df["Телефон 1"].astype(
        str)
    non_matching_df["Телефон 2"] = non_matching_df["Телефон 2"].astype(
        str)

    # return matching_df[["Наименование", "Веб-сайт 1", "Телефон 1", "Телефон 2"]], non_matching_df[["Наименование", "Веб-сайт 1", "Телефон 1", "Телефон 2"]]
    return matching_df["Веб-сайт 1"], non_matching_df["Веб-сайт 1"]


def create_driver():
    # Создание объекта ChromeOptions
    options = Options()

    # Установка опции для фонового режима
    options.add_argument('--headless')

    # Запуск браузера с заданными параметрами
    driver = webdriver.Chrome(options=options)
    return driver


def get_html(url, driver):
    try:
        driver.get(url)

        # Чтобы страница полностью загрузилась
        time.sleep(2)

        # Получаем содержимое страницы с помощью Selenium
        html = driver.page_source

    except Exception as e:
        print(f"Ошибка при открытии ссылки {url}: {e}")
        html = None

    return html


def parse_script_src(html):
    '''Парсит содержимое src внутри тега script и значение href внутри тега link только внутри блока head'''
    soup = BeautifulSoup(html, 'html.parser')
    head = soup.head
    script_tags = head.find_all('script')
    link_tags = head.find_all('link')

    for script in script_tags:
        src = str(script.get('src'))
        if 'yandex' in src or 'bitrix' in src or 'amo.crm' in src:
            return True

    for link in link_tags:
        href = str(link.get('href'))
        if 'yandex' in href or 'bitrix' in href or 'amo.crm' in href:
            return True

    return False


def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + '://' + parsed_url.netloc
    return base_url


def company_site_check():
    l1 = []
    l2 = []
    links1, links2 = get_company_links('1.xlsx')
    driver = create_driver()

    for link in links1:
        base_link = get_base_url(link)
        html = get_html(base_link, driver)
        if html is not None:
            if parse_script_src(html):
                l1.append(base_link)
            else:
                l2.append(base_link)
        else:
            l2.append(base_link)

    # Проверка и выравнивание длин списков l1 и l2
    max_len = max(len(l1), len(l2))
    l1 += [''] * (max_len - len(l1))
    l2 += [''] * (max_len - len(l2))

    # Создание DataFrame для сохранения результатов
    data = {
        "Компании с платными номерами (Sources)": l1,
        "Компании с платными номерами (Not sources)": l2
    }
    df1 = pd.DataFrame(data)

    l1 = []
    l2 = []

    for link in links2:
        base_link = get_base_url(link)
        html = get_html(base_link, driver)
        if html is not None:
            if parse_script_src(html):
                l1.append(base_link)
            else:
                l2.append(base_link)
        else:
            l2.append(base_link)

    # Проверка и выравнивание длин списков l1 и l2
    max_len = max(len(l1), len(l2))
    l1 += [''] * (max_len - len(l1))
    l2 += [''] * (max_len - len(l2))

    # Добавление результатов для links2 в DataFrame
    data = {
        "Компании с бесплатными номерами (Sources)": l1,
        "Компании с бесплатными номерами (Not sources)": l2
    }
    df2 = pd.DataFrame(data)

    # Запись DataFrame в Excel-файл
    with pd.ExcelWriter('результаты.xlsx') as writer:
        df1.to_excel(
            writer, sheet_name='Компании с платными номерами', index=False)
        df2.to_excel(
            writer, sheet_name='Компании с бесплатными номерами', index=False)

    driver.quit()


company_site_check()
