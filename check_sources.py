from chrome_driver import create_driver
from get_2gis_links import get_company_links

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains


def check_sources_links(links):
    driver = create_driver()
    sources_links = []
    for link in links:
        try:
            driver.get(link)
            # Нажатие клавиши Enter
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            # Нажатие клавиши Escape
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            # Получение HTML-кода страницы
            html = driver.page_source
            # Проверка наличия требуемых значений в блоке head
            if any(value in html for value in ['mc.yandex.ru', 'bitrix', 'amo.crm']):
                print(f'Сайт {link} использует метрики.')
                sources_links.append(link)
            else:
                print(f'Сайт {link} НЕ использует метрики.')
        except WebDriverException as e:
            print(f"Ошибка при обработке ссылки {link}")
    driver.quit()
    return sources_links


def get_source_links():
    print('\nЯ сказала стартуем! Чекаем есть ли на сайтах метрики:')
    links_tier_1, links_tier_2 = get_company_links('1.xlsx')
    sources_links_tier_1 = check_sources_links(links_tier_1)
    sources_links_tier_2 = check_sources_links(links_tier_2)
    return sources_links_tier_1, sources_links_tier_2