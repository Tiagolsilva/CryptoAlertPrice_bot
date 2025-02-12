import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, filters

# Configuração do Bot
TELEGRAM_BOT_TOKEN = "8127477680:AAFzs5tPpThWgo9PrCbLzjPli5FCqZczmpQ"

# Função para buscar os preços de BTC, ETH e SOL
def get_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd"
    response = requests.get(url)

    if response.status_code == 200:
        prices = response.json()
        btc_price = prices["bitcoin"]["usd"]
        eth_price = prices["ethereum"]["usd"]
        sol_price = prices["solana"]["usd"]

        return f"""
        🚀 **Preços das Criptomoedas:**
        🟡 **Bitcoin (BTC):** ${btc_price}
        🔵 **Ethereum (ETH):** ${eth_price}
        🟠 **Solana (SOL):** ${sol_price}
        """
    else:
        return "❌ Erro ao buscar os preços. Tente novamente mais tarde."

# Função que responde ao comando /start
async def start(update: Update, context):
    chat_id = update.message.chat_id
    first_name = update.message.from_user.first_name  

    message = f"Hello {first_name}, welcome to your bot! 🚀\nYour Chat ID is: `{chat_id}`"

    with open("chat_id.txt", "a") as file:
        file.write(f"{chat_id}\n")

    await update.message.reply_text(message, parse_mode="Markdown")

# Função que responde ao comando /prices
async def send_crypto_prices(update: Update, context):
    message = get_crypto_prices()
    await update.message.reply_text(message, parse_mode="Markdown")

# Configuração do bot usando a nova estrutura
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Adicionar comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prices", send_crypto_prices))

    print("🤖 Bot iniciado... Envie /start no Telegram!")
    app.run_polling()

if __name__ == "__main__":
    main()