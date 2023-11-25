import asyncio
import pandas as pd
from telegram import Bot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
config = dotenv_values('.env')

async def main():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    min_discount = chat_id = config.get('MIN_DISCOUNT')

    driver.get(f'https://www.kabum.com.br/ofertas/BLACKFRIDAY?pagina=1&desconto_minimo=' + min_discount + '&desconto_maximo=100')

    nameCards = driver.find_elements(By.CLASS_NAME, 'nameCard')
    priceCard = driver.find_elements(By.CLASS_NAME, 'priceCard')
    oldPriceCards = driver.find_elements(By.CLASS_NAME, 'oldPriceCard')
    discountTagCards = driver.find_elements(By.CLASS_NAME, 'discountTagCard')
    productLinks = driver.find_elements(By.CLASS_NAME, 'productLink')

    data = []

    for i in range(len(nameCards)):
        row = {
            'Nome': nameCards[i].text,
            'Preço': priceCard[i].text,
            'Preço Antigo': oldPriceCards[i].text,
            'Desconto': discountTagCards[i].text,
            'Link do Produto': productLinks[i].get_attribute('href')
        }
        data.append(row)

    df = pd.DataFrame(data)
    csv_filename = 'produtos.csv'
    df.to_csv(csv_filename, index=False, encoding='utf-8')
    print(f'Os dados foram salvos em {csv_filename}')

    telegram_token = config.get('TELEGRAM_TOKEN')
    chat_id = config.get('CHAT_ID')

    bot = Bot(token=telegram_token)
    with open(csv_filename, 'rb') as file:
        await bot.send_document(chat_id=chat_id, document=file)

if __name__ == "__main__":
    asyncio.run(main())