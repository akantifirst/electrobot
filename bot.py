import asyncio
from typing import Any, Dict
from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types import FSInputFile
import calc
import cad

router = Router()
project_data = {}


class Form(StatesGroup):
    start = State()
    name = State()
    extra_options = State()
    laying = State()
    add_feeder = State()
    project_info = State()
    maker = State()


# Entry point to fill in feeder data
@router.message(Form.add_feeder, F.text.casefold() == "ja")
@router.message(Form.start)
@router.message(commands={"nshv"})
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.name)
    await message.answer(
        f"Geben Sie bitte die Daten des Schaltschranks ein.\n"
        f"Alles ausser Leistung (oder Strom) ist optional.\n"
        f"<b>Beispiel:</b> <i>UV-AV-EG 23kw 56m</i>\n"
        "Siehe /hilfe für mehr Beispiele.",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )


# Cancel from any state
@router.message(commands={"/abbr"})
@router.message(F.text.casefold() == "abbr")
@router.message(F.text.casefold() == "abbruch")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    await state.clear()
    await message.answer(
        "Vorgang abgebrochen",
        reply_markup=ReplyKeyboardRemove(),
    )


# After all feeder data is provided, the user must provide project information
@router.message(Form.add_feeder, F.text.casefold() == "nein")
async def project_info(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.project_info)
    await message.answer(
        "Geben Sie bitte die Projektnummer und den Namen ein:\n"
        "<b>Beispiel:</b> <i>1025 Philharmonie Gasteig</i>",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )


# after all details to current feeder are provided,
# or if the user doesn't want to specify extra options,
# he is asked if he wants to add the next feeder
@router.message(Form.maker)
@router.message(Form.extra_options, F.text.casefold() == "nein")
async def next_feeder(message: Message, state: FSMContext) -> None:
    if message.text.casefold() not in ["ja", "nein"]:
        await state.update_data(maker=message.text)
    data = await state.get_data()
    try:
        await update_feeder(data=data)
    except TypeError:
        pass
    await state.clear()
    await state.set_state(Form.add_feeder)
    await message.answer(
        f"Gut. Wollen Sie noch einen Spannungsabgang hinzufügen?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Ja"),
                    KeyboardButton(text="Nein"),
                    KeyboardButton(text="Abbruch"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


# After required details such as name are provided,
# user is asked if he wants to provide additional details to this feeder
@router.message(Form.name)
async def extra_options(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    try:
        await state.set_state(Form.extra_options)
        await message.answer(
            f"Zusätzliche Parameter für den Schaltschrank\n"
            f"<b>{html.quote(message.text)}</b> angeben?",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Ja"),
                        KeyboardButton(text="Nein"),
                        KeyboardButton(text="Abbruch"),
                    ]
                ],
                resize_keyboard=True,
                parse_mode="HTML"
            ),
        )
    except (TypeError, ValueError):
        await message.reply('Please, review your request [bot]')


# After project info is provided, the user must give details about equipment maker
@router.message(Form.laying)
async def maker(message: Message, state: FSMContext) -> None:
    await state.update_data(laying=message.text)
    await state.set_state(Form.maker)
    await message.answer(
        "Bitte den Hersteller des Schutzorgans angeben."
        "\nVerwenden Sie bitte die Schaltflächen unten:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="ABB"),
                    KeyboardButton(text="Siemens"),
                    KeyboardButton(text="Hager")
                ]
            ],
            resize_keyboard=True,
        ),
    )


# after extra options are chosen, user asked to provide laying art
@router.message(Form.extra_options, F.text.casefold() == "ja")
async def laying(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.laying)
    await message.answer(
        "Wählen Sie bitte den Verlegeart des Kabels.\nVerwenden Sie bitte die Schaltflächen unten:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Im Erde")],
                [KeyboardButton(text="In einem Installationskanal")],
                [KeyboardButton(text="Auf einer Kabelwanne")],
                [KeyboardButton(text="Auf einer gelochter Kabelwanne")],
                [KeyboardButton(text="Im Luft")],
                [KeyboardButton(text="In wärmegedämmter Wand")],
                [KeyboardButton(text="Abbruch")]
            ],
            resize_keyboard=True,
        ),
    )


# After maker is provided, the calculation results are sent to user.
@router.message(Form.project_info)
async def send_results(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.update_data(project=message.text)
    data = await state.get_data()
    try:
        await update_feeder(data=data)
    except TypeError:
        pass
    await message.answer(
        "Fertig! Unten ist das NSHV-Schema und\n"
        "die NSHV-Berechnung in Tabellenform",
        reply_markup=ReplyKeyboardRemove()
        )
    await show_summary(message=message)
    project_data.clear()


# if input is incorrect
@router.message(Form.add_feeder)
@router.message(Form.extra_options)
async def review_request(message: Message) -> None:
    await message.reply("Überpüfen sie bitte die Richtigkeit ihrer Angaben.")


# append current feeder to project dictionary
async def update_feeder(data: Dict[str, Any]) -> None:
    number = len(project_data) + 1
    project_data[number] = data
    print(project_data)


# show content of project dictionary
@router.message(commands={"log"})
async def show_summary(message: Message) -> None:
    list_data = [' '.join([text for key, text in element.items()]) for number, element in project_data.items()]
    print(list_data)
    fdata = []
    for feeder in list_data[:-1]:
        parsed_data = calc.parse_input(feeder)
        computed_data = calc.calc(parsed_data)
        fdata.append(calc.format_values(computed_data))
        print(fdata)
    cad.cad_write(fdata)

    dxf_name = FSInputFile("output/template.dxf", filename="Schema.dxf")
    await message.answer_document(dxf_name)
    fdata.clear()
    await message.answer(str(list_data))


@router.message(commands=['help'])
async def process_help(message: Message):
    await message.reply('<b>12kw  => </b> <i>12kW 400V cos(φ)=0.95</i>\n'
                        '<b>12kW 0.8  => </b> <i>12kW 400V cos(φ)=0.8</i>\n'
                        '<b>12kW 230V 0.9  => </b> <i>12kW 230V cos(φ)=0.9</i>\n'
                        '<b>35a 230V 0.6  => </b> <i>35A 230V cos(φ)=0.6</i>\n'
                        '<b>12  => </b> <i>12kW 400V cos(φ)=0.95</i>', parse_mode='HTML')


@router.message(commands=['laying'])
async def process_laying(message: Message):
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


@router.message()
async def echo_message(message: Message):
    # Handling incorrect user input
    try:
        parsed_data = calc.parse_input(message.text)
        computed_data = calc.calc(parsed_data)
        fdata = calc.format_values(computed_data)
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

    except (TypeError, ValueError):
        await message.reply('Please, review your request [bot]')


async def main():
    bot = Bot(token="2110824051:AAEwlUouUFgTDI8Gkf8s6HN6xw9QPT1M9FU", parse_mode="HTML")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())