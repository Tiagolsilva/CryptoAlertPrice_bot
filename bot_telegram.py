import requests


TELEGRAM_BOT_TOKEN = "8127477680:AAFzs5tPpThWgo9PrCbLzjPli5FCqZczmpQ"
CHAT_ID = "7540701922"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        print("✅ Message sent successfully.") 
    else: 
        print(f"❌ Failed to send message. Error: {response.text}")

send_telegram_message("Hello, this is a test message from your bot!")