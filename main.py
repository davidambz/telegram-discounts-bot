import time
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

    min_discount = config.get('MIN_DISCOUNT')

    driver.get(f'https://www.kabum.com.br/ofertas/cybermonday?pagina=1&desconto_minimo=' + min_discount + '&desconto_maximo=100')

    while(len(driver.find_elements(By.CLASS_NAME, 'nameCard'))) == 0:
        time.sleep(1)

    nameCards = driver.find_elements(By.CLASS_NAME, 'nameCard')
    priceCard = driver.find_elements(By.CLASS_NAME, 'priceCard')
    oldPriceCards = driver.find_elements(By.CLASS_NAME, 'oldPriceCard')
    discountTagCards = driver.find_elements(By.CLASS_NAME, 'discountTagCard')
    productLinks = driver.find_elements(By.CLASS_NAME, 'productLink')

    telegram_token = config.get('TELEGRAM_TOKEN')
    chat_id = config.get('CHAT_ID')

    bot = Bot(token=telegram_token)

    for i in range(len(nameCards)):
        message = f'''
    <b>🚨 {nameCards[i].text.upper()}</b>
    <b>Com {discountTagCards[i].text} de desconto:</b>
    
    De: <s>{oldPriceCards[i].text}</s> | Por: <b>{priceCard[i].text}</b>

    <b>Link do Produto:</b>
    <a href="{productLinks[i].get_attribute('href')}">{nameCards[i].text}</a>
        '''

        await bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')

if __name__ == "__main__":
    asyncio.run(main())