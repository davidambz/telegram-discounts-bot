# Telegram Bot: Discounts at Kabum

This Python scripts is designed to scrape a website for product information, specifically looking for items on discount. When a new discounted product is found, it sends a notification to a specified Telegram chat with details about the product, including its name, price, discount, and a link to the product.

## Configuration

There should be a file named `sent_products.csv` at the root of the project with the following header:

| Nome | Preço | Preço Antigo | Desconto | Link do Produto | Data |
| ---- | ------ | ------------- | -------- | --------------- | ---- |

The script reads configuration details from a `.env` file using the `dotenv` library. It expects the following parameters:

* `LINK_SITE`: The URL of the website to scrape.
* `TELEGRAM_TOKEN`: Telegram Bot API token for authentication.
* `CHAT_ID`: The ID of the Telegram chat where notifications will be sent.

## Notes

* The script uses a headless Chrome browser to perform web scraping without a visible browser window.
* Notifications are sent in HTML format to Telegram, including the product image.
* Product information is tracked to avoid sending duplicate notifications.

## Usage

To use the script:

1. Install the required dependencies using poetry: `poetry install`.
2. Set up a `.env` file with the required configuration parameters.
3. Run the script: `poetry run python main.py`.


To clean the CSV file:

1. Execute o script: `poetry run python cleaning_csv.py`.

This command will delete files that have been sent more than a week ago.
