from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC

from chrome_driver import create_driver
from get_2gis_links import get_company_links


def check_sources_links(links):
    driver = create_driver()
    sources_links = []
    not_valid_links = []
    for link in links:
        try:
            driver.get(link)
            # Явное ожидание появления метрик в блоке head
            WebDriverWait(driver, 5).until(
                lambda driver: any(value in driver.page_source for value in ['mc.yandex.ru', 'bitrix', 'amo.crm', 'Jivo', 'calltouch'])
            )
            # Получение HTML-кода страницы
            html = driver.page_source
            # Проверка наличия требуемых значений в блоке head
            if any(value in html for value in ['mc.yandex.ru', 'bitrix', 'amo.crm', 'Jivo', 'calltouch']):
                print(f'Сайт {link} использует метрики.')
                sources_links.append(link)
            else:
                print(f'Сайт {link} НЕ использует метрики.')
        except WebDriverException as e:
            print(f"Ошибка при обработке ссылки {link}")
            not_valid_links.append(link)
    driver.quit()
    return sources_links, not_valid_links


def get_source_links():
    links_tier_1, links_tier_2 = get_company_links('1.xlsx')

    print('\nПлатные номера:')
    sources_links_1, not_valid_sources_links_1 = check_sources_links(links_tier_1[:100])
    print('\nБесплатные номера:')
    sources_links_2, not_valid_sources_links_2 = check_sources_links(links_tier_2[:100])

    return sources_links_1, sources_links_2, not_valid_sources_links_1, not_valid_sources_links_2