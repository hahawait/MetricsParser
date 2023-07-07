"""
Модуль для сохранения ссылок
"""
from openpyxl import Workbook


def save_links(
    valid_links_tier1, valid_links_tier2,
    invalid_sources_tier1, invalid_sources_tier2,
    invalid_visits_tier1, invalid_visits_tier2):
    """Метод сохраняет результаты в Excel файл"""

    # Создаем новую рабочую книгу
    workbook = Workbook()

    # Создаем листы
    sheet_valid = workbook.active
    sheet_valid.title = "Валидные ссылки"
    sheet_invalid = workbook.create_sheet(title="Невалидные ссылки")

    # Записываем заголовки столбцов на листе sheet_valid
    sheet_valid['A1'] = "Платные номера"
    sheet_valid['B1'] = "Количество посещений"
    sheet_valid['C1'] = "Бесплатные номера"
    sheet_valid['D1'] = "Количество посещений"

    # Записываем данные в соответствующие столбцы на листе sheet_valid
    for i, (link_tier1, visits_tier1) in enumerate(valid_links_tier1):
        sheet_valid['A' + str(i+2)] = link_tier1
        sheet_valid['B' + str(i+2)] = visits_tier1

    for i, (link_tier2, visits_tier2) in enumerate(valid_links_tier2):
        sheet_valid['C' + str(i+2)] = link_tier2
        sheet_valid['D' + str(i+2)] = visits_tier2

    # Записываем заголовки столбцов на листе sheet_invalid
    sheet_invalid['A1'] = "Не валидные Sources (платные номера)"
    sheet_invalid['B1'] = "Не валидные Sources (бесплатные номера)"
    sheet_invalid['C1'] = "Не валидные Similar (платные номера)"
    sheet_invalid['D1'] = "Не валидные Similar (бесплатные номера)"

    # Записываем данные в соответствующие столбцы на листе sheet_invalid
    for i, not_valid_s in enumerate(invalid_sources_tier1):
        sheet_invalid['A' + str(i+2)] = not_valid_s

    for i, not_valid_s in enumerate(invalid_sources_tier2):
        sheet_invalid['B' + str(i+2)] = not_valid_s

    for i, not_valid_v in enumerate(invalid_visits_tier1):
        sheet_invalid['C' + str(i+2)] = not_valid_v

    for i, not_valid_v in enumerate(invalid_visits_tier2):
        sheet_invalid['D' + str(i+2)] = not_valid_v

    # Сохраняем файл
    workbook.save("Ссылки.xlsx")
