import os
import requests

BOT_TOKEN = os.environ.get('BOT_TOKEN', '8570719163:AAERxF81IzlEWEPUgh6L0jZUlpUwcBV7nrc')
CHAT_ID = os.environ.get('CHAT_ID', '-1003723920541')

def test_api():
    print("🔍 Testing Telegram API...")
    print(f"BOT_TOKEN: {BOT_TOKEN[:10]}...")
    print(f"CHAT_ID: {CHAT_ID}")
    
    # Method 1: getMe
    print("\n📡 Method 1: Checking bot...")
    response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getMe")
    print(f"Bot Status: {response.json()}")
    
    # Method 2: sendMessage
    print("\n📤 Method 2: Sending message...")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": "🚀 Test from GitHub Actions",
        "parse_mode": "Markdown"
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    if result.get("ok"):
        print("✅ Message sent successfully!")
        print(f"Message ID: {result['result']['message_id']}")
        return True
    else:
        print(f"❌ Failed: {result.get('description')}")
        return False

if __name__ == "__main__":
    success = test_api()
    exit(0 if success else 1)