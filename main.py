import telebot
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from telebot import types
tokken = '5687118516:AAFDJEYMN1kXi5WaOJcjYOk-r9vGr4aozJs'
bot = telebot.TeleBot(tokken)
@bot.message_handler(commands=["start"])
def start(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Назначить встречу')
    button2 = types.KeyboardButton('Да')
    button3 = types.KeyboardButton('Нет')
    markup.add(button1, button2, button3,)
    bot.send_message(m.chat.id,"Здравствуйте, {0.first_name}!".format(m.from_user), reply_markup=markup)
    bot.send_message(m.chat.id, 'Я Ваш виртуальный помощник!/help')
@bot.message_handler(content_types=['text'])
def get_text_messages(m):
    calendar, step = DetailedTelegramCalendar().build()
    if m.text == "/help":
        bot.send_message(m.chat.id, "Назначить встречу?")
    if m.text == "Да":
        bot.send_message(m.chat.id, "На какое число?")
        bot.send_message(m.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)
    if m.text == "Нет":
        bot.send_message(m.chat.id, "Хорошо, как понадобится помощь напишите /help")
    if m.text == "Назначить встречу":
        bot.send_message(m.chat.id, "На какое число?")
        bot.send_message(m.chat.id, f"Select {LSTEP[step]}",reply_markup=calendar)
@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}", c.message.chat.id, c.message.message_id, reply_markup=key)
    elif result:
        bot.edit_message_text(f"Вы выбрали {result}", c.message.chat.id, c.message.message_id)
bot.polling(none_stop=True, interval=0)
