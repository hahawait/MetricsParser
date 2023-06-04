import pandas as pd
from urllib.parse import urlparse


def get_company_links(filename):
    # Загрузка Excel-таблицы
    df = pd.read_excel(filename)

    # Удаление дубликатов
    df = df.drop_duplicates(subset=["Наименование"])
    df = df.drop_duplicates(subset=["Веб-сайт 1"])

    # Удаление компаний у которых нет сайта
    df = df.dropna(subset=["Веб-сайт 1"])

    # Конвертация столбцов с номерами телефонов в строки
    df["Телефон 1"] = df["Телефон 1"].astype(str)
    df["Телефон 2"] = df["Телефон 2"].astype(str)

    # Удлание параметров из ссылок (сотавляем только базовый url)
    df["Веб-сайт 1"] = df["Веб-сайт 1"].apply(lambda url: urlparse(url).scheme + "://" + urlparse(url).netloc)

    # Фильтрация по номерам телефонов
    match_num = ('8800', '8495', '8812')
    condition = df["Телефон 1"].astype(str).str.startswith(
        match_num) | df["Телефон 2"].astype(str).str.startswith(match_num)
    matching_df = df[condition]
    non_matching_df = df[~condition]

    return matching_df["Веб-сайт 1"], non_matching_df["Веб-сайт 1"]