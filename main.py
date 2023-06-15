import time
from openpyxl import Workbook

from check_sources import get_source_links
from check_visits_nums import get_valid_links


def save_to_excel(valid_links_tier1, valid_links_tier2):
    # Создаем новую рабочую книгу
    workbook = Workbook()
    # Получаем активный лист
    sheet = workbook.active

    # Записываем заголовки столбцов
    sheet['A1'] = "Платные номера"
    sheet['B1'] = "Количество посещений"
    sheet['C1'] = "Бесплатные номера"
    sheet['D1'] = "Количество посещений"

    # Записываем данные в соответствующие столбцы
    for i, (link_tier1, visits_tier1) in enumerate(valid_links_tier1):
        sheet['A' + str(i+2)] = link_tier1
        sheet['B' + str(i+2)] = visits_tier1

    for i, (link_tier2, visits_tier2) in enumerate(valid_links_tier2):
        sheet['C' + str(i+2)] = link_tier2
        sheet['D' + str(i+2)] = visits_tier2

    # Сохраняем файл
    workbook.save("Ссылки.xlsx")


def main():
    start_time = time.time()

    # Чекаем метрики
    sources_links_tier_1, sources_links_tier_2 = get_source_links()
    print(f"\nВремя выполнения проверки метрик: {(round(time.time() - start_time, 2)) / 60} минут")

    start_time = time.time()

    # Чекаем визиты
    print('\nЧекаем количество посещений на сайтах с подключенными метриками')
    print('\nПлатные номера:')
    valid_links_tier1 = get_valid_links(sources_links_tier_1)
    print('\nБесплатные номера:')
    valid_links_tier2 = get_valid_links(sources_links_tier_2)
    save_to_excel(valid_links_tier1, valid_links_tier2)
    print(f"\nВремя выполнения получения количества посещений: {(round(time.time() - start_time, 2)) / 60} минут")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"\n\nОбщее время выполнения: {(round(time.time() - start_time, 2)) / 60} минут")
    print('\n\n\n\n\nКороче, ситуация такая')
