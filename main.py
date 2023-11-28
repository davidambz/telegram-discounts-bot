import time
import asyncio
import pandas as pd
from telegram import Bot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
from datetime import datetime

config = dotenv_values('.env')

async def wait_for_element(driver, by, value, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        elements = driver.find_elements(by, value)
        if elements:
            return elements
        time.sleep(1)
    raise TimeoutError(f"Element {value} not found after {timeout} seconds")

async def main():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920x1080')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(config.get('LINK_SITE'))

    telegram_token = config.get('TELEGRAM_TOKEN')
    chat_id = config.get('CHAT_ID')

    bot = Bot(token=telegram_token)

    csv_file = 'sent_products.csv'
    try:
        existing_data = pd.read_csv(csv_file)
        sent_products = set(existing_data['Nome'])
    except (FileNotFoundError, KeyError):
        existing_data = pd.DataFrame(columns=['Nome', 'Preço', 'Preço Antigo', 'Desconto', 'Link do Produto', 'Data'])
        sent_products = set()

    while True:
        await wait_for_element(driver, By.CLASS_NAME, 'nameCard')

        nameCards = driver.find_elements(By.CLASS_NAME, 'nameCard')
        priceCard = driver.find_elements(By.CLASS_NAME, 'priceCard')
        oldPriceCards = driver.find_elements(By.CLASS_NAME, 'oldPriceCard')
        discountTagCards = driver.find_elements(By.CLASS_NAME, 'discountTagCard')
        productLinks = driver.find_elements(By.CLASS_NAME, 'productLink')
        images_url = driver.find_elements(By.CLASS_NAME, 'imageCard')

        for i in range(len(nameCards)):
            product_name = nameCards[i].text
            if product_name in sent_products:
                driver.quit()
                return

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            message = f'''
<b>🚨 {product_name.upper()}</b>
<b>Com {discountTagCards[i].text} de desconto:</b>

De: <s>{oldPriceCards[i].text}</s> | Por: <b>{priceCard[i].text}</b>

<b>Link do Produto:</b>
<a href="{productLinks[i].get_attribute('href')}">{product_name}</a>
            '''

            await bot.send_photo(chat_id=chat_id, photo=images_url[i].get_attribute('src'), caption=message, parse_mode='HTML')

            new_data = pd.DataFrame({
                'Nome': [product_name],
                'Preço': [priceCard[i].text],
                'Preço Antigo': [oldPriceCards[i].text],
                'Desconto': [discountTagCards[i].text],
                'Link do Produto': [productLinks[i].get_attribute('href')],
                'Data': [current_time]
            })
            existing_data = pd.concat([existing_data, new_data], ignore_index=True)
            existing_data.to_csv(csv_file, index=False)

            time.sleep(1)

        next_page_button = driver.find_element(By.XPATH, '//*[@id="PaginationOffer"]/button')
        if not next_page_button.is_enabled():
            print("Não há mais páginas. Parando o script.")
            driver.quit()
            return

        next_page_button.click()
        time.sleep(30)

if __name__ == "__main__":
    asyncio.run(main())
