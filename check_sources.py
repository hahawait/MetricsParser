import time
import asyncio


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains


from get_2gis_links import get_company_links


async def check_link(link, valid_links, driver):
    try:
        time.sleep(0.2)
        driver.get(link)
        time.sleep(0.2)
        # Нажатие клавиши Enter
        ActionChains(driver).send_keys(Keys.ENTER).perform()
        # Нажатие клавиши Escape
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(0.2)
        # Получение HTML-кода страницы
        html = driver.page_source
        
        # Проверка наличия требуемых значений в блоке head
        if any(value in html for value in ['mc.yandex.ru', 'bitrix', 'amo.crm']):
            valid_links.append(link)
    except WebDriverException as e:
        print(f"Ошибка при обработке ссылки {link}: {e}")


async def process_links(links, valid_links, driver):
    tasks = []
    for link in links:
        task = asyncio.create_task(check_link(link, valid_links, driver))
        tasks.append(task)

    await asyncio.gather(*tasks)


async def get_source_links():
    driver = webdriver.Chrome()
    # driver.set_page_load_timeout(3)  # Установка тайм-аута
    links_tier_1, links_tier_2 = get_company_links('1.xlsx')

    valid_links_tier_1 = []
    valid_links_tier_2 = []
    
    await process_links(links_tier_1, valid_links_tier_1, driver)
    await process_links(links_tier_2, valid_links_tier_2, driver)
    print(valid_links_tier_1)
    driver.quit()
    return valid_links_tier_1, valid_links_tier_2


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(get_source_links())
    print(f"Время выполнения: {round(time.time() - start_time, 2)} секунд")
