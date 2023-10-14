import time
import webbrowser
import sqlite3
import telebot
from telebot import types

bot = telebot.TeleBot('6414097305:AAHWXSqx6CLHRKH6YCGWm4jityJeyabCvlQ')

startText = (
    "Добро пожаловать в Тулпар Бот Проезда!\n\n"
    "🚍 ОПЛАЧИВАЙ ПРОЕЗД С УДОВОЛЬСТВИЕМ!\n"
    "💎 Копите баллы и обменивайте их на скидки, оплату услуг или даже игровой донат!\n"
    "📚 ПОМОЩЬ И ИНФОРМАЦИЯ:\n"
    " /help - Получить список доступных команд.\n"
    "\nСпасибо за использование Тулпар Бот Проезда! Приятной поездки!"
)


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            name VARCHAR(49) NOT NULL,
            balance REAL DEFAULT 0,
            points INTEGER DEFAULT 0,
            trips INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, startText)
    time.sleep(2)
    bot.send_message(message.chat.id, 'Вас нужно зарегистрировать! Введите ваше имя')
    bot.register_next_step_handler(message, surname)

def surname(message):
    name = message.text.strip()
    UserName = '@' + message.from_user.username
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()

    cur.execute('INSERT INTO users (username, name) VALUES (?, ?)', (UserName, name))
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!')


@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, 'help info')
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    uss = cur.fetchall()

    info = ''
    for el in uss:
        info += f'Имя: {el[3]} '

    cur.close()
    conn.close()

    bot.send_message(message.chat.id, info)

# open site
@bot.message_handler(commands=['website'])
def openSite(message):
    webbrowser.open('https://github.com/BayelChieftain')

# user data in chat
@bot.message_handler()
def info(message):
    fName = message.from_user.first_name
    UserName = '@' + message.from_user.username
    bot.send_message(message.chat.id, UserName)

bot.polling(none_stop=True)