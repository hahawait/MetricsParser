from openpyxl import Workbook


def save_links(valid_links_tier1, valid_links_tier2, not_valid_s_1, not_valid_s_2, not_valid_v_1, not_valid_v_2):
    # Создаем новую рабочую книгу
    workbook = Workbook()
    # Получаем активный лист
    sheet = workbook.active

    # Записываем заголовки столбцов
    sheet['A1'] = "Платные номера"
    sheet['B1'] = "Количество посещений"
    sheet['C1'] = "Бесплатные номера"
    sheet['D1'] = "Количество посещений"
    sheet['E1'] = "Не валидные Sources (платные номера)"
    sheet['F1'] = "Не валидные Sources (бесплатные номера)"
    sheet['G1'] = "Не валидные Similar (платные номера)"
    sheet['H1'] = "Не валидные Similar (бесплатные номера)"

    # Записываем данные в соответствующие столбцы
    for i, (link_tier1, visits_tier1) in enumerate(valid_links_tier1):
        sheet['A' + str(i+2)] = link_tier1
        sheet['B' + str(i+2)] = visits_tier1

    for i, (link_tier2, visits_tier2) in enumerate(valid_links_tier2):
        sheet['C' + str(i+2)] = link_tier2
        sheet['D' + str(i+2)] = visits_tier2

    for i, not_valid_s in enumerate(not_valid_s_1):
        sheet['E' + str(i+2)] = not_valid_s

    for i, not_valid_s in enumerate(not_valid_s_2):
        sheet['F' + str(i+2)] = not_valid_s

    for i, not_valid_v in enumerate(not_valid_v_1):
        sheet['G' + str(i+2)] = not_valid_v

    for i, not_valid_v in enumerate(not_valid_v_2):
        sheet['H' + str(i+2)] = not_valid_v

    # Сохраняем файл
    workbook.save("Ссылки.xlsx")

