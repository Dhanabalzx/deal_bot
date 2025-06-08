import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot

# Load secrets from environment
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = os.getenv("TELEGRAM_CHANNEL")
BITLY_TOKEN = os.getenv("BITLY_TOKEN")

bot = Bot(token=BOT_TOKEN)

HEADERS = {"User-Agent": "Mozilla/5.0"}

# Sample Ajio category (men jeans)
AJIO_URL = "https://www.ajio.com/men-jeans/c/830216002"

def shorten_link(long_url):
    headers = {
        'Authorization': f'Bearer {BITLY_TOKEN}',
        'Content-Type': 'application/json'
    }
    json_data = {"long_url": long_url}
    response = requests.post("https://api-ssl.bitly.com/v4/shorten", headers=headers, json=json_data)
    return response.json().get("link", long_url)

def scrape_ajio():
    response = requests.get(AJIO_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "lxml")

    items = soup.select(".item")
    for item in items[:5]:  # Only first 5 items for demo
        try:
            name = item.select_one(".nameCls").text.strip()
            brand = item.select_one(".brand").text.strip()
            price = item.select_one(".price .orginal-price").text.strip()
            offer_price = item.select_one(".price .price-value").text.strip()
            discount = item.select_one(".discount").text.strip()
            link = "https://www.ajio.com" + item.a['href']
            short_link = shorten_link(link)

            msg = f"🔥 {brand} - {name}\n💰 Offer: {offer_price} | MRP: {price}\n🔖 {discount}\n🛒 Buy: {short_link}"
            post_to_telegram(msg)
        except Exception as e:
            print("Error in parsing an item:", e)

def post_to_telegram(message):
    try:
        bot.send_message(chat_id=CHANNEL, text=message, parse_mode="HTML")
    except Exception as e:
        print("Telegram Error:", e)

if __name__ == "__main__":
    scrape_ajio()
