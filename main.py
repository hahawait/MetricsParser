import time

from check_sources import get_source_links
from check_visits_nums import get_valid_links
from save_links import save_links


def main():
    target_nums = input('\nВведите количество тысяч посещений для фильтрации сайтов: ')

    # Чекаем метрики
    print('\nЧекаем есть ли на сайтах метрики')
    start_time = time.time()
    sources_links_tier_1, sources_links_tier_2, not_valid_s_1, not_valid_s_2 = get_source_links()
    print(f"\nВремя выполнения проверки метрик: {round(((time.time() - start_time) / 60), 2)} минут")

    # Чекаем визиты
    print('\nЧекаем количество посещений на сайтах с подключенными метриками')
    start_time = time.time()
    print('\nПлатные номера:')
    valid_links_tier1, not_valid_v_1 = get_valid_links(sources_links_tier_1, target_nums)
    print('\nБесплатные номера:')
    valid_links_tier2, not_valid_v_2 = get_valid_links(sources_links_tier_2, target_nums)
    save_links(valid_links_tier1, valid_links_tier2, not_valid_s_1, not_valid_s_2, not_valid_v_1, not_valid_v_2)

    print(f"\nВремя выполнения получения количества посещений: {round(((time.time() - start_time) / 60), 2)} минут")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"\n\nОбщее время выполнения: {round(((time.time() - start_time) / 60), 2)} минут")

    input('Нажмите Enter для закрытия консоли')
