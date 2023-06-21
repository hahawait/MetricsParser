import time

from get_2gis_links import get_company_links
from check_sources import check_sources_links
from check_visits_nums import transform_links, get_visits_value, check_visits_value
from save_links import save_links
from chrome_driver import create_driver


def get_visits_links(sources_links, target_nums, driver):
    similar_links = transform_links(sources_links)
    visits_num = get_visits_value(similar_links, driver)
    valid_links, invalid_links = check_visits_value(sources_links, visits_num, target_nums)

    return valid_links, invalid_links


def get_result(links, target_nums, driver):
    print('\nЧекаем есть ли на сайтах метрики:')
    sources_urls_1, invalid_sources_urls = check_sources_links(links, driver)
    print('\nЧекаем количество посещений сайтов на similar:')
    visits_urls, invalid_visits_urls = get_visits_links(sources_urls_1, target_nums, driver)

    return invalid_sources_urls, visits_urls, invalid_visits_urls


def main():
    # Получаем ссылки сайтов из файла
    urls_tier_1, urls_tier_2 = get_company_links('1.xlsx')
    # Пользователь вводит нужное значение
    target_nums = input('\nВведите количество тысяч посещений для фильтрации сайтов: ')

    driver = create_driver()

    print('\nПлатные номера:')
    n_sources_urls_1, valid_urls_1, invalid_urls_1 = get_result(urls_tier_1, target_nums, driver)

    print('\nБесплатные номера:')
    n_sources_urls_2, valid_urls_2, invalid_urls_2 = get_result(urls_tier_2, target_nums, driver)

    driver.quit()

    # Сохраняем результаты
    save_links(
        valid_urls_1, valid_urls_2,
        n_sources_urls_1, n_sources_urls_2,
        invalid_urls_1, invalid_urls_2
    )


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"\n\nВремя выполнения: {round(((time.time() - start_time) / 60), 2)} минут")

    input('Нажмите Enter для закрытия консоли...\n')
