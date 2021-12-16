import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.types import FSInputFile
from config import TOKEN
import cad
import calc

dp = Dispatcher()


@dp.message(commands=['start'])
async def process_start(message: types.Message):
    await message.reply('Welcome to power/current converter. \n'
                        'Please enter either current (add suffix A) or power (add suffix kW).\n'
                        'Optionally you can enter voltage (add suffix V).\n'
                        'and power factor (a number from 0.5 to 1).\n\n'
                        'Example:\n    <i>12kw 230v,\n    20a 0.8,\n    34kw 400V 0.95</i>\n'
                        'Type /help for more examples.', parse_mode='HTML')


@dp.message(commands=['help'])
async def process_help(message: types.Message):
    await message.reply('<b>12kw  => </b> <i>12kW 400V cos(φ)=0.95</i>\n'
                        '<b>12kW 0.8  => </b> <i>12kW 400V cos(φ)=0.8</i>\n'
                        '<b>12kW 230V 0.9  => </b> <i>12kW 230V cos(φ)=0.9</i>\n'
                        '<b>35a 230V 0.6  => </b> <i>35A 230V cos(φ)=0.6</i>\n'
                        '<b>12  => </b> <i>12kW 400V cos(φ)=0.95</i>', parse_mode='HTML')


@dp.message(commands=['laying'])
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


@dp.message()
async def echo_message(message: Message):
    # Handling incorrect user input
    try:
        parsed_data = calc.parse_input(message.text)
        computed_data = calc.calc(parsed_data)
        fdata = calc.format_values(computed_data)
        cad.cad_write([fdata])
        name, power, g, phi, voltage, cable, section, length, du, laying, cb, cb_type, release, ib = fdata
        await message.answer(f'<code>Verteiler:     {name}\n'
                             f'Leistung:      {power}\n'
                             f'Gleichz.-keit: {g}\n'
                             f'cos(f):        {phi}\n'
                             f'Spannung:      {voltage}\n'
                             f'Kabel:         {cable}\n'
                             f'Querschnitt:   {section}\n'
                             f'Kabellänge:    {length}\n'
                             f'Spannungsfall: {du}\n'
                             f'Verlegeart:    {laying}\n'
                             f'Schutzorgan:   {cb}\n'
                             f'S.-organ Typ:  {cb_type}\n'
                             f'Auslöser:      {release}\n'
                             f'Ausl.-strom:   {ib}</code>',
                             parse_mode='HTML')
        fdata.clear()
        dxf_name = FSInputFile("template.dxf", filename="Schema.dxf")
        await message.reply_document(dxf_name)
    except (TypeError, ValueError):
        await message.reply('Please, review your request [bot]')


async def main():
    bot = Bot(token=TOKEN, parse_mode="HTML")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
