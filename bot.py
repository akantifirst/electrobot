import telebot
from calc import calc

bot = telebot.TeleBot('1779223371:AAFDFO38aEeVMCZzT4tSe1VczuFk4y-OCB4')


@bot.message_handler(commands=['help', 'start'])
def start_command(message):
    bot.send_message(message.chat.id,
                     'Welcome to power/current converter. \n'
                     'Please enter either current (add suffix A) or power (add suffix kW),\n'
                     'and optionally voltage and power factor.\n'
                     'Type /help for some examples')


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def request_message(message):
    try:
        power, current, voltage, power_factor = calc(message.text)
        bot.reply_to(message, f'P = {power:.1f} kW, \n'
                              f'I = {current:.1f} A, \n'
                              f'U =  {voltage:.0f} V, \n'
                              f'cos(φ) = {power_factor:.2f}')
    except TypeError:
        bot.reply_to(message, 'Please, review your request')


bot.polling()
