import yfinance as yf
import pandas as pd
import requests

# --- إعدادات التنبيه (اختياري) ---
TOKEN = "ضعي_التوكن_هنا_إذا_أردت_تلغرام"
CHAT_ID = "ضع_الـID_هنا"

def send_telegram(message):
    if TOKEN != "ضعي_التوكن_هنا_إذا_أردت_تلغرام":
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

def analyze():
    print("--- 🔍 نظام CleanWave Alpha: جاري الفحص عبر Yahoo Finance ---")
    try:
        # جلب بيانات البيتكوين (رمزها في ياهو هو BTC-USD)
        # نطلب بيانات آخر يومين بفريم 15 دقيقة
        ticker = yf.Ticker("BTC-USD")
        df = ticker.history(period="2d", interval="15m")
        
        if df.empty:
            print("❌ فشل جلب البيانات. جاري المحاولة مرة أخرى...")
            return

        # حساب المؤشرات (نفس منطق استراتيجيتك)
        df['ema_8'] = df['Close'].ewm(span=8, adjust=False).mean()
        df['ema_21'] = df['Close'].ewm(span=21, adjust=False).mean()
        
        last_price = df['Close'].iloc[-1]
        ema8 = df['ema_8'].iloc[-1]
        ema21 = df['ema_21'].iloc[-1]

        print(f"💰 السعر الحالي: ${round(last_price, 2)}")
        
        # اتخاذ القرار
        if ema8 > ema21:
            result = "🚀 اتجاه صاعد (Bullish)"
        else:
            result = "📉 اتجاه هابط/عرضي (Bearish)"
            
        print(f"📊 النتيجة: {result}")
        
        # إرسال التقرير
        report = f"🔔 *تحديث CleanWave Alpha*\n💰 السعر: ${round(last_price, 2)}\n📊 الحالة: {result}"
        send_telegram(report)
        
    except Exception as e:
        print(f"❌ خطأ فني: {e}")

if __name__ == "__main__":
    analyze()
