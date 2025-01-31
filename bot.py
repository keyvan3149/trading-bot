import os
import time
import ccxt
import requests
from dotenv import load_dotenv
import subprocess

# بارگذاری متغیرهای محیطی
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not API_KEY or not API_SECRET or not TELEGRAM_TOKEN or not CHAT_ID:
    print("❌ API Keys یا Telegram Config یافت نشد! لطفاً فایل .env را بررسی کنید.")
    exit()

# تنظیم صرافی LBank
exchange = ccxt.lbank({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'options': {'defaultType': 'spot'}
})

# ارسال پیام تلگرام
def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

# دریافت نماد صحیح
def get_correct_symbol():
    try:
        markets = exchange.load_markets()
        if "BTC/USDT" in markets:
            return "BTC/USDT"
        send_telegram_message("❌ BTC/USDT not found in LBank symbols!")
        return None
    except Exception as e:
        send_telegram_message(f"❌ Error fetching symbols: {e}")
        return None

# دریافت دقت و حداقل مقدار
def get_precision_and_min_amount(symbol):
    try:
        markets = exchange.load_markets()
        if symbol in markets:
            precision = markets[symbol]["precision"]["amount"]
            min_amount = markets[symbol]["limits"]["amount"]["min"]
            return precision, min_amount
        send_telegram_message(f"❌ Error: Trading pair {symbol} not found!")
        return None, None
    except Exception as e:
        send_telegram_message(f"❌ Error fetching precision data: {e}")
        return None, None

# اجرای سفارش خرید
def open_position(symbol, amount, precision, min_amount):
    try:
        if amount < min_amount:
            send_telegram_message(f"❌ Amount {amount} is less than minimum {min_amount}")
            return None

        amount = round(amount, precision)
        amount = float(amount)

        order = exchange.create_order(symbol, "market", "buy", amount)
        send_telegram_message(f"✅ Order placed: {order}")
        return order
    except ccxt.PermissionDenied:
        send_telegram_message("❌ API Key Permission Denied! بررسی کنید API Key درست تنظیم شده باشد.")
        fix_and_restart()
    except ccxt.NetworkError:
        send_telegram_message("❌ Network Error! اینترنت را بررسی کنید.")
        fix_and_restart()
    except Exception as e:
        send_telegram_message(f"❌ Error opening buy position: {e}")
        fix_and_restart()

# **آپدیت خودکار ربات**
def update_bot():
    send_telegram_message("🔄 در حال بررسی آپدیت جدید...")

    try:
        # دانلود آخرین نسخه از گیت‌هاب (یا هر سورس دیگر)
        repo_url = "https://github.com/نام-کاربری-گیتهاب/مخزن-ربات.git"
        subprocess.run(["git", "pull", repo_url], check=True)

        send_telegram_message("✅ آپدیت انجام شد! در حال ری‌استارت...")

        # ری‌استارت ربات
        restart_bot()
    except Exception as e:
        send_telegram_message(f"❌ خطا در آپدیت ربات: {e}")

# **ری‌استارت ربات**
def restart_bot():
    send_telegram_message("🔄 ربات در حال ری‌استارت است...")
    subprocess.run(["python3", "bot.py"])

# **تابع اصلاح و ری‌استارت خودکار**
def fix_and_restart():
    send_telegram_message("🛠 ربات در حال اصلاح خطا و ری‌استارت است...")

    # بررسی کنید آیا آپدیت جدید لازم است
    update_bot()

# اجرای ربات
def trading_bot():
    send_telegram_message("🚀 Trading bot started...")

    symbol = get_correct_symbol()
    if not symbol:
        send_telegram_message("❌ Symbol not found. Exiting...")
        return

    precision, min_amount = get_precision_and_min_amount(symbol)
    if precision is None or min_amount is None:
        send_telegram_message("❌ Failed to fetch precision/minimum amount. Exiting...")
        return

    while True:
        try:
            open_position(symbol, 0.001, precision, min_amount)
            time.sleep(180)  
        except Exception as e:
            send_telegram_message(f"❌ Error in bot execution: {e}")
            fix_and_restart()

if __name__ == "__main__":
    trading_bot()
