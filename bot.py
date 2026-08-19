import os
import threading
import telebot
from flask import Flask
from datetime import datetime, date

TOKEN = '8787056666:AAFRnwg1xGmVihvSYJyWooLNRPQV-mLj8EU'
bot = telebot.TeleBot(TOKEN)

# رقم الآيدي الخاص بك للتنبيهات
ADMIN_CHAT_ID = 1085878578  

REQUIRED_CHAT = '@telebotksu'

months_ar = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", 
             "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]

# دالة حساب موعد المكافأة والأيام الباقية
def get_reward_countdown():
    today = date.today()
    target_date = date(2026, 8, 27) # موعد إيداع مكافأة أغسطس
    
    delta = target_date - today
    days_left = delta.days
    
    if days_left < 0:
        return "تم إيداع المكافأة أو أن الموعد قد فات."
    
    date_str = target_date.strftime("%Y-%m-%d")
    return f"مُتوقع إيداع مكافأة شهر أغسطس يوم الموافق [{date_str}م] [بعد {days_left} أيام ]"

# دالة التحقق من اشتراك المستخدم في القناة
def check_membership(user_id):
    try:
        member = bot.get_chat_member(REQUIRED_CHAT, user_id)
        if member.status in ['creator', 'administrator', 'member']:
            return True
    except Exception as e:
        print(f"Error checking membership: {e}")
    return False

# أمر /start (يعرض الترحيب + عداد المكافأة)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    if not check_membership(user_id):
        bot.reply_to(message, f"عذراً، يجب عليك الاشتراك في القناة أولاً: {REQUIRED_CHAT}")
        return

    countdown_text = get_reward_countdown()
    reply_text = f"أهلاً بك! 🚀\n\n{countdown_text}"
    bot.reply_to(message, reply_text)

# دالة تحويل رسائل المستخدمين لك (مع تجاهل رسائلك أنت)
@bot.message_handler(func=lambda message: True)
def forward_to_admin(message):
    if message.from_user.id == ADMIN_CHAT_ID:
        return
        
    user = message.from_user
    text = message.text or "[محتوى ليس نصاً]"
    
    log_text = (
        f"📩 رسالة جديدة من مستخدم:\n\n"
        f"👤 الاسم: {user.first_name} {user.last_name or ''}\n"
        f"🔗 اليوزر: @{user.username or 'لا يوجد'}\n"
        f"🆔 الآيدي: `{user.id}`\n\n"
        f"💬 الرسالة:\n{text}"
    )
    
    try:
        bot.send_message(ADMIN_CHAT_ID, log_text, parse_mode="Markdown")
    except Exception as e:
        print(f"Error forwarding to admin: {e}")

# إعداد خادم Flask البسيط للبقاء نشطاً على Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

if __name__ == '__main__':
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    print("Bot is polling...")
    bot.infinity_polling()
