from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import token
from calc import calc

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Welcome to power/current converter. \n'
                        'Please enter either current (add suffix A) or power (add suffix kW).\n'
                        'Optionally you can enter voltage (add suffix V).\n'
                        'and power factor (a number from 0.5 to 1).\n\n'
                        'Example:\n    <i>12kw 230v,\n    20a 0.8,\n    34kw 400V 0.95</i>\n'
                        'Type /help for more examples.', parse_mode='HTML')


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply('<b>12kw  => </b> <i>12kW 400V cos(φ)=0.95</i>\n'
                        '<b>12kW 0.8  => </b> <i>12kW 400V cos(φ)=0.8</i>\n'
                        '<b>12kW 230V 0.9  => </b> <i>12kW 230V cos(φ)=0.9</i>\n'
                        '<b>35a 230V 0.6  => </b> <i>35A 230V cos(φ)=0.6</i>\n'
                        '<b>12  => </b> <i>12kW 400V cos(φ)=0.95</i>', parse_mode='HTML')


@dp.message_handler()
async def echo_message(msg: types.Message):
    # Handling incorrect user input
    try:
        power, current, voltage, power_factor = calc(msg.text)
        await bot.send_message(msg.from_user.id, f'P = <b>{power:.1f}</b> kW, \n'
                                                 f'I = <b>{current:.1f}</b> A, \n'
                                                 f'<i>U = {voltage:.0f} V, \n'
                                                 f'cos(φ) = {power_factor:.2f}</i>', parse_mode='HTML')
    except TypeError:
        await msg.reply('Please, review your request')


if __name__ == '__main__':
    executor.start_polling(dp)
