import os
import threading
import telebot
from flask import Flask
from datetime import datetime

TOKEN = '8787056666:AAFRmwg1xGmViHvSYJyMooLNRPQV-mLjBEU'
bot = telebot.TeleBot(TOKEN)

# مصفوفة بأسماء الأشهر
months_ar = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", 
             "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'أهلاً بك! أنا بوت تذكير مكافأة جامعة الملك سعود.\nاستخدم /status لمعرفة الموعد.')

@bot.message_handler(commands=['status'])
def send_status(message):
    now = datetime.now()
    
    # تحديد تاريخ المكافأة القادم (يوم 27 من الشهر الحالي)
    target_date = datetime(now.year, now.month, 27)
    
    # إذا كان اليوم قد تجاوز يوم 27، نحسب الشهر القادم
    if now.day > 27:
        if now.month == 12:
            target_date = datetime(now.year + 1, 1, 27)
        else:
            target_date = datetime(now.year, now.month + 1, 27)
            
    delta = target_date - now
    days_left = delta.days
    month_name = months_ar[target_date.month - 1]
    
    msg = (f"مُتوقع إيداع مكافأة شهر {month_name} يوم\n"
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
