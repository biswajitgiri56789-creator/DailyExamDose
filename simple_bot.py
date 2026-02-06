import os
import sys
import requests

def main():
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    CHAT_ID = os.environ.get('CHAT_ID')
    
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ BOT_TOKEN or CHAT_ID not set!")
        sys.exit(1)
    
    print(f"✅ BOT_TOKEN found: {BOT_TOKEN[:10]}...")
    print(f"✅ CHAT_ID: {CHAT_ID}")
    
    # Create message
    message = """
🎯 *Daily Exam Dose - LIVE NOW!* 🎯

✅ *Status:* Bot is Active
📅 *Date:* Today
🕐 *Time:* Now
📚 *Subjects:* Bengali & English
🏫 *Classes:* 11, 12, College
🚀 *Schedule:* Every 30 minutes

🔢 *Question #:* 1
❓ *Question:* What is the capital of Bangladesh?
*A.* Dhaka
*B.* Chittagong
*C.* Sylhet
*D.* Rajshahi

✅ *Answer:* A

📌 *Note:* This is a test question.
"""
    
    # Send via API
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        result = response.json()
        
        if result.get("ok"):
            print(f"✅ Success! Message ID: {result['result']['message_id']}")
            return True
        else:
            print(f"❌ Telegram API Error: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Request Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)