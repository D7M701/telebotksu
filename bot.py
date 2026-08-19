import os
import threading
import telebot
from flask import Flask
from datetime import datetime

TOKEN = '8787056666:AAFRnwg1xGmVihvSYJyWooLNRPQV-mLj8EU'
bot = telebot.TeleBot(TOKEN)

# حط رقم الآيدي الخاص بك هنا (مثلاً: 123456789)
ADMIN_CHAT_ID = 1085878578  

REQUIRED_CHAT = '@telebotksu'

months_ar = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", 
             "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]

# دالة للتحقق مما إذا كان المستخدم عضواً في القناة/القروب
def check_membership(user_id):
    try:
        member = bot.get_chat_member(REQUIRED_CHAT, user_id)
        if member.status in ['creator', 'administrator', 'member']:
            return True
    except Exception as e:
        print(f"Error checking membership: {e}")
    return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    # تحقق من الاشتراك
    if not check_membership(user_id):
        bot.reply_to(message, f"عذراً، يجب عليك الاشتراك في القناة أولاً: {REQUIRED_CHAT}")
        return

    bot.reply_to(message, "أهلاً بك في بوت مؤقت المكافأة!")

# دالة استقبال وتحويل أي رسالة نصية أخرى لك
@bot.message_handler(func=lambda message: True)
def forward_to_admin(message):
    # تجاهل رسائل الآدمن نفسه عشان ما يصير تكرار
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

# إعداد خادم Flask بسيط للبقاء نشطاً على Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

if __name__ == '__main__':
    # تشغيل سيرفر Flask في خيط مستقل
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    # تشغيل البوت
    print("Bot is polling...")
    bot.infinity_polling()
