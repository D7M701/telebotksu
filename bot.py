import os
import telebot
from flask import Flask

# رمز بوت تيليجرام حقك
TOKEN = '8787056666:AAFRnwg1xGmVihvSYJyWooLNRPQV-mLj8EU'  # حط التوكن حقك هنا إذا لم يكن محفوظاً في مكان آخر
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(message, 'أهلاً بك! تم تشغيل البوت بنجاح 🚀')


# اعداد سيرفر الويب الوهمي عشان يرضى Render
app = Flask('')


@app.route('/')
def home():
  return 'I am alive!'


if __name__ == '__main__':
  # تشغيل بوت تيليجرام بخلفية بسيطة أو تشغيل السيرفر
  import threading

  def run_bot():
    bot.infinity_polling()

  t = threading.Thread(target=run_bot)
  t.start()

  # تشغيل سيرفر الويب على البورت المطلوب
  port = int(os.environ.get('PORT', 10000))
  app.run(host='0.0.0.0', port=port)
