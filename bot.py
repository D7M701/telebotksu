import os
import threading
import telebot
from flask import Flask

TOKEN = '8787056666:AAFRmwg1xGmViHvSYJyMooLNRPQV-mLjBEU'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(message, 'أهلاً بك! تم تشغيل البوت بنجاح 🚀')


# اعداد سيرفر الويب الوهمي عشان يرضى Render
app = Flask('')


@app.route('/')
def home():
  return 'I am alive!'


def run_bot():
  bot.infinity_polling()


if __name__ == '__main__':
  # تشغيل البوت في مسار جانبي (Thread)
  t = threading.Thread(target=run_bot)
  t.start()

  # تشغيل السيرفر على البورت المطلوب
  port = int(os.environ.get('PORT', 10000))
  app.run(host='0.0.0.0', port=port)
