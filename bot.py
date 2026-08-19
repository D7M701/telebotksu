import os
import threading
import telebot
from flask import Flask
from datetime import datetime

TOKEN = '8787056666:AAFRnwg1xGmVihvSYJyWooLNRPQV-mLj8EU'
bot = telebot.TeleBot(TOKEN)

# حط هنا معرف القناة أو القروب الإجباري (مثلاً '@ChannelName' أو '-100xxxxxxxxxx')
REQUIRED_CHAT = '@telebotksu'

months_ar = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", 
             "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]

# دالة للتحقق مما إذا كان المستخدم عضو في القناة/القروب
def check_membership(user_id):
    try:
        member = bot.get_chat_member(REQUIRED_CHAT, user_id)
        # إذا كانت حالة المستخدم من ضمن المسموح لهم
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
        bot.reply_to(message, f"عذراً, يجب عليك الانضمام إلى القناة/القروب أولاً لكي يعمل معك البوت:\n{REQUIRED_CHAT}\n\nبعد الانضمام، ارسل /start مجدداً.")
        return

    # إذا اشترك، تطلع له رسالة الترحيب أو المكافأة مباشرة
    now = datetime.now()
    target_date = datetime(now.year, now.month, 27)
    if now.day > 27:
        if now.month == 12:
            target_date = datetime(now.year + 1, 1, 27)
        else:
            target_date = datetime(now.year, now.month + 1, 27)
            
    delta = target_date - now
    days_left = delta.days
    month_name = months_ar[target_date.month - 1]
    
    msg = (f"أهلاً بك! 🚀\n\n"
           f"مُتوقع إيداع مكافأة شهر {month_name} يوم\n"
           f"الموافق [2026-{target_date.month:02d}-27م] [بعد {days_left + 1} أيّام ]")
    bot.reply_to(message, msg)

app = Flask('')
@app.route('/')
def home():
    return 'I am alive!'

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    t = threading.Thread(target=run_bot)
    t.start()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
