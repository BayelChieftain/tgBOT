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
helpText = (
    "/balance - Проверить текущий баланс и количество баллов.\n"
    "/profile - Посмотреть свой профиль.\n" 
    "/help - Получить список доступных команд.\n"
    "/pay - Пополнить баланс\n"
    "/ticket - Оплата проезда\n"
)

def CheckBalance(userName, msg):
    import sqlite3

    conn = sqlite3.connect('users.sql')
    cursor = conn.cursor()

    # Имя пользователя, для которого нужно получить баланс
    username_to_lookup = userName

    # Выполнение запроса
    cursor.execute("SELECT balance, points FROM users WHERE username = ?", (username_to_lookup,))
    result = cursor.fetchone()
    if result:
        balance, points = result
        bot.send_message(msg.chat.id, f"Ваш баланс:  {balance}\nКоличество баллов:  {points}")
    else:
        bot.send_message(msg.chat.id, f"Пользователь {username_to_lookup} не найден.")

    conn.close()

def CheckProfile(userName, msg):
    conn = sqlite3.connect('users.sql')
    cursor = conn.cursor()

    username_to_lookup = userName
    cursor.execute('SELECT name, trips FROM users WHERE username = ?', (username_to_lookup,))
    result = cursor.fetchone()

    if result:
        name, trips = result
        bot.send_message(msg.chat.id, f"Имя пользователя: {name}\nКоличество поездок пользователя: {trips}")
    else:
        print(f"Пользователь {username_to_lookup} не найден.")

    conn.close()

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
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
    cur.execute('INSERT OR IGNORE INTO users (username, name) VALUES (?, ?)', (UserName, name))
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!')

@bot.message_handler(commands=['balance'])
def balance(msg):
    userName = '@' + msg.from_user.username
    bot.send_message(msg.chat.id, CheckBalance(userName, msg))

@bot.message_handler(commands=['profile'])
def profile(msg):
    userName = '@' + msg.from_user.username
    bot.send_message(msg.chat.id, CheckProfile(userName, msg))

@bot.message_handler(commands=['help'])
def main(message):

    bot.send_message(message.chat.id, helpText)

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
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('11 сом', callback_data='11'))
    markup.add(types.InlineKeyboardButton('33 сом', callback_data='33'))
    markup.add(types.InlineKeyboardButton('66 сом', callback_data='66'))
    markup.add(types.InlineKeyboardButton('88 сом', callback_data='88'))
    bot.send_message(message.chat.id, 'Пополнить баланс на сумму:', reply_markup=markup)
bot.polling(none_stop=True)