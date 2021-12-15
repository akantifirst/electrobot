import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import Message
import calc
from config import TOKEN

form_router = Router()


@form_router.message(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Welcome to power/current converter. \n'
                        'Please enter either current (add suffix A) or power (add suffix kW).\n'
                        'Optionally you can enter voltage (add suffix V).\n'
                        'and power factor (a number from 0.5 to 1).\n\n'
                        'Example:\n    <i>12kw 230v,\n    20a 0.8,\n    34kw 400V 0.95</i>\n'
                        'Type /help for more examples.', parse_mode='HTML')


@form_router.message(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply('<b>12kw  => </b> <i>12kW 400V cos(φ)=0.95</i>\n'
                        '<b>12kW 0.8  => </b> <i>12kW 400V cos(φ)=0.8</i>\n'
                        '<b>12kW 230V 0.9  => </b> <i>12kW 230V cos(φ)=0.9</i>\n'
                        '<b>35a 230V 0.6  => </b> <i>35A 230V cos(φ)=0.6</i>\n'
                        '<b>12  => </b> <i>12kW 400V cos(φ)=0.95</i>', parse_mode='HTML')


@form_router.message(commands=['laying'])
async def process_help_command(message: types.Message):
    await message.reply('<b>A1</b> <i> - in Installationsrohren in wärmegedämmten Wänden</i>\n'
                        '<b>A2</b> <i> - in Installationsrohren in wärmegedämmten Wänden; Mehradrig</i>\n'
                        '<b>B1</b> <i> - in Installationsrohren auf einer Wand</i>\n'
                        '<b>B2</b> <i> - in Installationsrohren auf einer Wand; Mehradrig</i>\n'
                        '<b>C1</b> <i> - direkt auf einer Wand</i>\n'
                        '<b>D1</b> <i> - in Erde</i>\n'
                        '<b>E1</b> <i> - Installationskanal</i>\n'
                        '<b>F1</b> <i> - auf gelochter Kabelwanne mit Berührung; Einadrig</i>\n'
                        '<b>F2</b> <i> - auf gel. Kabelwanne mit Berührung; Eine Schicht; Mehradrig</i>\n'
                        '<b>F3</b> <i> - auf gel. Kabelwanne mit Berührung; Mehrere Schichte; Mehradrig</i>\n'
                        '<b>G1</b> <i> - auf gel. Kabelwanne ohne Berührung; Horizontal</i>\n'
                        '<b>G2</b> <i> - auf gel. Kabelwanne ohne Berührung; Vertikal</i>\n', parse_mode='HTML')


@form_router.message()
async def echo_message(message: Message):
    try:
        parsed_data = calc.parse_input(message.text)
        computed_data = calc.calc(parsed_data)
        fdata = calc.format_values(computed_data)

        await message.answer(f'<code>Verteiler:     {fdata[0]}\n'
                             f'Leistung:      {fdata[1]}\n'
                             f'Strom:         {fdata[2]}\n'
                             f'Spannung:      {fdata[3]}\n'
                             f'cos(φ):        {fdata[4]}\n'
                             f'Kabel:         {fdata[7]} {fdata[6]}({fdata[8]}) {fdata[11]}\n'
                             f'Verlegeart:    {fdata[5]}\n'
                             f'Schutzorgan:   {fdata[14]}\n'
                             f'Spannungsfall: {fdata[13]}</code>',
                             parse_mode='HTML')
    except (TypeError, ValueError):
        await message.reply('Please, review your request [bot]')


async def main():
    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_router(form_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

