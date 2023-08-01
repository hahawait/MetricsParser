import time
import asyncio

from src.utils.chrome_driver import create_driver
from src.data.save_to_excel import save_links
from src.data.two_gis_links import get_company_links
from src.parser.visits_nums import check_visits_value
from src.parser.sources_links import check_sources_link


async def get_result(links, target_nums):
    '''Фильтрует валидные ссылки'''
    driver = await create_driver()

    valid = []
    invalid_sources = []
    invalid_visits = []
    try:
        for link in links:
            try:
                source_link = await check_sources_link(link, driver)
                if source_link is True:
                    visits = await check_visits_value(link, driver, target_nums)
                    if isinstance(visits, str):
                        valid.append((link, visits))
                    elif visits is None:
                        invalid_visits.append(link)
                elif source_link is False:
                    invalid_sources.append(link)
            except Exception as e:
                print(f'Ошибка внутри цикла обработки: {e}')
                driver.quit()
                driver = await create_driver()
                continue
    except Exception as e:
        print(f'Ошибка вне цикла обработки: {e}')
    finally:
        driver.quit()
        return valid, invalid_sources, invalid_visits


async def main():
    # Получаем ссылки сайтов из файла
    urls_tier_1, urls_tier_2 = get_company_links('1.xlsx')
    # Пользователь вводит нужное значение
    target_nums = input(
        '\nВведите количество тысяч посещений для фильтрации сайтов: ')

    print('\nПлатные номера:')
    valid_1, invalid_sources_1, invalid_visits_1 = await get_result(
        urls_tier_1, target_nums)

    print('\nБесплатные номера:')
    valid_2, invalid_sources_2, invalid_visits_2 = await get_result(
        urls_tier_2, target_nums)

    # Сохраняем результаты
    save_links(
        valid_1, valid_2,
        invalid_sources_1, invalid_sources_2,
        invalid_visits_1, invalid_visits_2
    )


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    print(
        f"\nВремя выполнения: {round(((time.time() - start_time) / 60), 2)} минут")

    input('\nНажмите Enter для закрытия консоли...\n')
