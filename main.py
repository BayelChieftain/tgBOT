import webbrowser

import telebot

bot = telebot.TeleBot('xxx')



@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'It works')


@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, 'help info')

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