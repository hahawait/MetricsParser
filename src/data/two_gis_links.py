"""
Модуль для работы с исходным xlsx файлом.
"""
import pandas as pd
from urllib.parse import urlparse


def get_company_links(filename):
    """
    Метод удаляет дубликаты и возвращает два списка сайтов компаний.
    Первый с платными номерами телефонов, второй с бесплатными
    """

    # Загрузка Excel-таблицы
    data_frame = pd.read_excel(filename)

    # Удаление дубликатов
    data_frame = data_frame.drop_duplicates(subset=["Наименование"])
    data_frame = data_frame.drop_duplicates(subset=["Веб-сайт 1"])

    # Удаление компаний у которых нет сайта
    data_frame = data_frame.dropna(subset=["Веб-сайт 1"])

    # Удаление параметров из ссылок (оcтавляем только базовый url)
    data_frame["Веб-сайт 1"] = data_frame["Веб-сайт 1"].apply(
        lambda url: urlparse(url).scheme + "://" + urlparse(url).netloc)

    # Конвертация столбцов с номерами телефонов в строки
    data_frame["Телефон 1"] = data_frame["Телефон 1"].astype(str)
    data_frame["Телефон 2"] = data_frame["Телефон 2"].astype(str)

    # Фильтрация по номерам телефонов
    match_num = ('8800', '8495', '8812')
    condition = data_frame["Телефон 1"].str.startswith(
        match_num) | data_frame["Телефон 2"].str.startswith(match_num)

    matching_df = data_frame[condition]
    non_matching_df = data_frame[~condition]

    return matching_df["Веб-сайт 1"], non_matching_df["Веб-сайт 1"]
