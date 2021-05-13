import config
import telebot  # install package as pyTelegramBotAPI
from calc import calc

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id,
                     'Welcome to power/current converter. \n'
                     'Please enter either current (add suffix A) or power (add suffix kW).\n'
                     'Optionally you can enter voltage (add suffix V).\n'
                     'and power factor (a number from 0.5 to 1).\n\n'
                     'Example:\n    <i>12kw 230v,\n    20a 0.8,\n    34kw 400V 0.95</i>\n'
                     'Type /help for more examples.', parse_mode='HTML')


@bot.message_handler(commands=['help'])
def start_command(message):
    bot.send_message(message.chat.id,
                     '<b>12kw  => </b> <i>12kW 400V cos(φ)=0.95</i>\n'
                     '<b>12kW 0.8  => </b> <i>12kW 400V cos(φ)=0.8</i>\n'
                     '<b>12kW 230V 0.9  => </b> <i>12kW 230V cos(φ)=0.9</i>\n'
                     '<b>35a 230V 0.6  => </b> <i>35A 230V cos(φ)=0.6</i>\n'
                     '<b>12  => </b> <i>12kW 400V cos(φ)=0.95</i>', parse_mode='HTML')


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def request_message(message):
    try:
        power, current, voltage, power_factor = calc(message.text)
        bot.reply_to(message, f'P = <b>{power:.1f}</b> kW, \n'
                              f'I = <b>{current:.1f}</b> A, \n'
                              f'<i>U = {voltage:.0f} V, \n'
                              f'cos(φ) = {power_factor:.2f}</i>', parse_mode='HTML')
    except TypeError:
        bot.reply_to(message, 'Please, review your request')


bot.polling()
