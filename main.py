import time

from get_2gis_links import get_company_links
from check_sources import check_sources_links
from check_visits_nums import transform_links, get_visits_value, check_visits_value
from save_links import save_links


def get_result(links, target_nums):
    print('\nЧекаем есть ли на сайтах метрики:')
    sources_urls_1, invalid_sources_urls = check_sources_links(links)

    print('\nЧекаем количество посещений сайтов на similar:')
    similar_links = transform_links(sources_urls_1)
    visits_num = get_visits_value(similar_links)
    visits_urls, invalid_visits_urls = check_visits_value(sources_urls_1, visits_num, target_nums)

    return invalid_sources_urls, visits_urls, invalid_visits_urls


def main():
    # Получаем ссылки сайтов из файла
    urls_tier_1, urls_tier_2 = get_company_links('1.xlsx')
    # Пользователь вводит нужное значение
    target_nums = input('\nВведите количество тысяч посещений для фильтрации сайтов: ')

    print('\nПлатные номера:')
    invalid_sources_urls_1, valid_urls_1, invalid_urls_1 = get_result(urls_tier_1, target_nums)

    print('\nБесплатные номера:')
    invalid_sources_urls_2, valid_urls_2, invalid_urls_2 = get_result(urls_tier_2, target_nums)

    # Сохраняем результаты
    save_links(
        valid_urls_1, valid_urls_2,
        invalid_sources_urls_1, invalid_sources_urls_2,
        invalid_urls_1, invalid_urls_2
    )


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"\n\nВремя выполнения: {round(((time.time() - start_time) / 60), 2)} минут")

    input('Нажмите Enter для закрытия консоли...\n')
