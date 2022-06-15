import os
from flask import Flask, request
import telebot
from telebot import types
import mysql.connector

TOKEN = '5464338504:AAFXhaac7qyQLZlzRUCCv-z7lSi5t-yjTug'
APP_URL = f'https://quqpuline.herokuapp.com/{TOKEN}'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
"""
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="test"
)"""

conn = mysql.connector.connect(
    host="srv-pleskdb49.ps.kz",
    port="3306",
    user="izderkz_magzhan",
    password="@Magzhan1201199445",
    database="izderkz_database"
)

cursor = conn.cursor()

"""==============================================DATABASE_FINISH==================================================="""

Fakultet1 = "Педагогика және психология институты"
Fakultet2 = "Қазақ тілі және әлем тілдері институты"
Fakultet3 = "Физика, математика және цифрлық \nтехнологиялар институты"
Fakultet4 = "Жаратылыстану институты"
Fakultet5 = "Әлеуметтік, гуманитарлық ғылымдар \nжәне өнер институты"
Fakultet6 = "Университет құрамындағы кәсіптік \nбілім беру колледжі"
Fakultet7 = "Магистратура және Докторантура"

kezekInBtn = "Кезекке тұру"
kezekOutBtn = "Кезектен шығу"
stopBot = "Ботты тоқтату"
homePage = "Бастапқы бетке оралу"
showKezek = "Нөмір қабылдануда!"


@bot.message_handler(commands=['start'])
def first(message):
    keyboard = types.ReplyKeyboardMarkup(True,False)
    keyboard.add('Мәзір')
    send = bot.send_message(message.chat.id, 'Сәлеметсіз бе! Бұл қабылдау комиссиясына кезекке тұру боты! Мәзірді басып, өз факультетіңізді таңдаңыз!',reply_markup=keyboard)
    bot.register_next_step_handler(send,second)

def second(message):
    if message.text == 'Мәзір':
        keyboard = types.ReplyKeyboardMarkup(True,False)
        keyboard.add(Fakultet1)
        keyboard.add(Fakultet2)
        keyboard.add(Fakultet3)
        keyboard.add(Fakultet4)
        keyboard.add(Fakultet5)
        keyboard.add(Fakultet6)
        keyboard.add(Fakultet7)
        keyboard.add(homePage)
        send = bot.send_message(message.chat.id,'Таңдаңыз!', reply_markup=keyboard)
        bot.register_next_step_handler(send,third)
    else:
        bot.send_message(message.chat.id,'Төменде орналасқан \nмәзірдегі батырманы басыңыз')


@bot.message_handler(content_types=['text'])
def third(message):
    """===============================Fakultetter==================================================="""
    #=================================FAKULTET_1========================================================
    if message.text == Fakultet1:
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.add(kezekInBtn)
        keyboard.add(showKezek)
        keyboard.add(kezekOutBtn)
        keyboard.add(homePage)
        keyboard.add(stopBot)
        send = bot.send_message(message.chat.id,
                                'Кезекке тұрсаңаз болады!',
                                reply_markup=keyboard)
        bot.register_next_step_handler(send, fakultetF1)


def fakultetF1(message):

    if message.text == kezekInBtn:
        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_sname = message.from_user.last_name
        username = message.from_user.username

        id_input = us_id
        with conn.cursor() as cursor:
            sql = 'INSERT INTO db_f_1 (user_id, user_name, user_surname, username) VALUES (%s, %s, %s, %s)'
            data = (us_id, us_name, us_sname, username)
            cursor.execute(sql, data)
            cursor.fetchall()
            conn.commit()


        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.add(kezekInBtn)
        keyboard.add(showKezek)
        keyboard.add(kezekOutBtn)
        keyboard.add(homePage)
        keyboard.add(stopBot)
        send = bot.send_message(message.chat.id, '- - - - - - - - - - - - - - - - - - - ', reply_markup=keyboard)
        bot.register_next_step_handler(send, fakultetF1)

        for result in cursor:
            print(result[0])

        bot.send_message(message.chat.id, 'Сіздің кезегіңіз қабылданды!')
        bot.send_message(message.chat.id, "Кезек нөмірі: " + str(result[0]))
"""
bot.polling(none_stop=True)

if __name__ == '__main__':
    bot.infinity_polling()"""


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return '!', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
