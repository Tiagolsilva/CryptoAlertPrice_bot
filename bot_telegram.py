import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Configs
TELEGRAM_BOT_TOKEN = "Your Telegram Bot Token"
API_KEY = "Your CoinMarketCap API Key"

def get_crypto_prices():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    parameters = {
        'start': '10',
        'limit': '2',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }

    response = requests.get(url, headers=headers, params=parameters)

    print(f"URL: {url}")  
    print(f"Status Code: {response.status_code}")  
    print(f"Response: {response.text}") 

    if response.status_code == 200:
        data = response.json()
        prices = {coin['symbol']: coin['quote']['USD']['price'] for coin in data['data']}
        
        btc_price = prices.get('BTC', "❌ Error: Bitcoin price not found.")
        eth_price = prices.get('ETH', "❌ Error: Ethereum price not found.")

        if isinstance(btc_price, float):
            btc_price = f"{btc_price:.2f}"
        if isinstance(eth_price, float):
            eth_price = f"{eth_price:.2f}"

        return f"""
        🚀 **Preços das Criptomoedas:**
        🟡 **Bitcoin (BTC):** ${btc_price}
        🔵 **Ethereum (ETH):** ${eth_price}
        """
    else:
        return "❌ Error fetching prices. Please try again later."

async def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    first_name = update.message.from_user.first_name  

    message = f"Hello {first_name}, welcome to your bot! 🚀\nYour Chat ID is: `{chat_id}`"

    with open("chat_id.txt", "a") as file:
        file.write(f"{chat_id}\n")

    await update.message.reply_text(message, parse_mode="Markdown")

async def send_crypto_prices(update: Update, context: CallbackContext):
    message = get_crypto_prices()
    await update.message.reply_text(message, parse_mode="Markdown")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prices", send_crypto_prices))

    print("🤖 Bot init... Send /start in Telegram!")
    app.run_polling()

if __name__ == "__main__":
    main()