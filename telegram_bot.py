import requests

# توکن ربات تلگرام (توکن خودتان را اینجا وارد کنید)
TELEGRAM_BOT_TOKEN = "8004631837:AAFslnP3nn6_fGjc7ZTeVJFcCx5_ei-pBoU"

# آیدی چت تلگرام شما (در مراحل بعد نحوه دریافت آن را توضیح می‌دهم)
CHAT_ID = "YOUR_CHAT_ID_HERE"

def send_telegram_message(message):
    """
    ارسال پیام به تلگرام
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("پیام با موفقیت ارسال شد!")
    else:
        print(f"خطا در ارسال پیام: {response.status_code}, {response.text}")
TELEGRAM_CHAT_ID =101253267
