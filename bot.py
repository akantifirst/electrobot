# Common python libraries
import re
import asyncio
from typing import Any

# Frameworks
from aiogram import (
    Bot,
    Dispatcher,
    F)
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import (
    State,
    StatesGroup)
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    FSInputFile)

# Project files
from config import (
    TOKEN,
    LAYING_TYPES,
    LAYING)
from common import (
    keyboard_laying,
    laying_provided,
    load_provided,
    get_name)
from calc import (
    parse_input,
    calc,
    format_values,
    parse_project,
    summary)


dispatcher = Dispatcher()
project_data = []
laying_types = LAYING_TYPES
laying = LAYING


# TODO:
#  check if it is possible to calculate without tables
#  move from csv files to redis database
#  add "options" section
#  add "verlegearten"
#  add possibility expand frame based on number of feeders
#  solve text scaling problem with Matplotlib backend
#  add generation of a report in Excel with xlwings
#  add generation of a report in pdf

# States for Finite State Machine
class Form(StatesGroup):
    feeder = State()
    laying = State()
    project = State()


@dispatcher.message(F.text.casefold().in_({'/abbr', 'abbr', 'abbruch'}))
async def process_cancel(message: Message, state: FSMContext) -> None:
    if await state.get_state() is not None:
        await state.clear()
        await message.answer("Vorgang ist vom Benutzer abgebrochen", reply_markup=ReplyKeyboardRemove())
        project_data.clear()


@dispatcher.message(F.text.casefold().in_({'/start', '/hilfe', 'start', 'hilfe'}))
async def process_help(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('<b>Willkomen zu Electrobot</b>.\n\n'
                         'Dieses Program ist geeignet um schnell den Kabelquerschnitt, den Spannungsfall, '
                         'oder den LS-Schalter sowie andere Parameter für ein oder auch für mehrere '
                         'Stromkreise zu ermitteln. Das Programm hat 2 Modi:\n',
                         reply_markup=ReplyKeyboardRemove(),
                         parse_mode='HTML')

    await message.answer('<b>Modus 1. Schnelle Kalkulation</b>\n\n'
                         'Schnelle Kalkulation eines Spannungsabgangs mit Ergebniss im Textform. '
                         'Tragen Sie bitte einfach die Nennleistung oder den Nennstrom ein. '
                         'Groß- und Kleinschreibung spielen hier keine Rolle.\n\n'
                         'Beispiel: <i>"23kw"</i> <b>oder</b> <i>"45a"</i>\n\n'
                         'Zusätzlich kann man andere Parameter, wie z.B. Kabellänge, '
                         'Verlegeart, oder zulässiger Spannungsfall, definieren.\n\n'
                         'Еine vollständige Liste der möglichen Optionen ist per Befehl /param verfügbar. '
                         'Wenn die in der Benutzereingabe fehlen, werden in der Berechnung '
                         'die Ursprungsparameter (siehe /optionen) benutzt.\n',
                         reply_markup=ReplyKeyboardRemove(),
                         parse_mode='HTML')

    await message.answer('<b>Modus 2. Hauptverteilerberechnung</b>\n\n'
                         'Hauptverteilerberechnung (mehrere Spannungsabgänge) mit Ergebnis im Form eines '
                         'Schemas im <b>CAD</b> Dateiformat.\n\n'
                         'Um zu diesen Modi zu wechseln, muss der Befehl <b>"/hv"</b> eingegeben werden. '
                         'In diesem Modi ist die sequentielle Eingabe von mehreren Stromkreisen möglich. '
                         'Die Parameter jedes Stromkreises werden in einzeilige Eingabe angegeben, wie '
                         'auch im Modi 1.\n\n'
                         'Nach Eingabe der Parameter des Stromkreises wird der Benutzer aufgefordert, einen '
                         'anderen Stromkreis einzugeben oder die Berechnung abzuschliessen. Nachdem alle '
                         'Stromkreise eingegeben sind, muss der Nummer und der Name des Projekts eingegeben '
                         'werden.\n\n'
                         'Im Schluss bekommt man die Berechnung im Form eines Schemata sowie eine tabellarische '
                         'Auflistung aller Stromkreise.',
                         reply_markup=ReplyKeyboardRemove(),
                         parse_mode='HTML')


@dispatcher.message(F.text.casefold().in_({'/param', 'param'}))
async def process_param(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('<b>Stromkreis Parameter</b>\n\n'
                         'Die folgende Stromkreisparameter kann man '
                         '(mit Leerzeichen getrennt) optional eingeben:\n\n'
                         '<b>Unterverteiler Name:</b>\n\n'
                         'Beliebige Name. Wenn vorhanden, muss ohne Leerzeichen als erstes Wort im\n '
                         'Eingabe angegeben werden.\n'
                         '<i>Beispiel: <b>uv-av-01</b></i>\n\n'
                         '<b>Kabeltyp:</b>\n\n'
                         'Folgende Kabeltypen werden derzeit unterstützt: NYY, NYCWY, NYM, NHXH.\n'
                         '<i>Beispiel: nycwy</i>\n\n'
                         '<b>Spannung des Stromkreises:</b>\n\n'
                         'Eine Zahl mit dem Suffix "v"\n'
                         '<i>Beispiel: 400v, 415v, 230v, 220v</i>\n\n'
                         '<b>Kabellänge des Stromkreises:</b>\n\n'
                         'Eine Zahl mit dem Suffix "m"\n'
                         '<i>Beispiel: 30m, 156m, 10m, 50m</i>\n\n'
                         '<b>Verlegeart des Kabels:</b>\n\n'
                         'Verlegearten siehe /verl\n'
                         'A1, A2, B1, B2, C1, E1 usw.\n'
                         '<i>Beispiel: a1, a2, c1, f1, f2</i>\n\n'
                         '<b>Leitermaterial:</b>\n\n'
                         'Folgende Leitermateriale werden \nderzeit unterstützt: Cu, Alu. \n'
                         '<i>Beispiel: cu, alu</i>\n\n'
                         '<b>Hersteller des Schutzorgans:</b>\n\n'
                         'Folgende Hersteller werden \nunterstützt: '
                         'ABB, Siemens, Hager\n'
                         '<i>Beispiel: abb, siemens, hager</i>\n\n'
                         '<b>Zulässiger Spannungsfall:</b>\n\n'
                         'Eine Zahl mit dem Suffix "%"\n'
                         '<i>Beispiel: 4%, 2.5%, 0.5%</i>\n\n'
                         '<b>Leistungsfaktor cos(f):</b>\n\n'
                         'Eine Zahl von 0,5 bis 1,0 ohne Suffix\n'
                         '<i>Beispiel: 0.76, 0.98, 0.95</i>\n\n'
                         '<b>Gleichzeitigkeitsfaktor:</b>\n\n'
                         'eine Zahl mit dem Suffix "g"\n'
                         '<i>Beispiel: <b>0.65g, 0.4g</b></i>\n\n'

                         'Alle Parameter, ausser Nennstrom oder Nennleistung, sind optional. '
                         'Wenn die in Benutzereingabe fehlen, werden für die Berechnung '
                         'die Ursprungparameter benutzt. '
                         'Die Optionen siehe unter /opt',
                         reply_markup=ReplyKeyboardRemove(),
                         parse_mode='HTML')


@dispatcher.message(F.text.casefold().in_({'/opt', 'opt'}))
async def process_param(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Diese Sektion ist derzeit in Bearbeitung ',
                         reply_markup=ReplyKeyboardRemove(),
                         parse_mode='HTML')


@dispatcher.message(Form.feeder, F.text.casefold() == "fertig")
async def process_project(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.project)
    await message.answer("Geben Sie bitte die Projektnummer und den Namen ein.\n"
                         "Optional geben Sie die UV-Name mit Komma getrennt ein.\n"
                         "<i>Beispiel: 1025 Philharmonie Gasteig, NSHV-BK1</i>",
                         reply_markup=ReplyKeyboardRemove())


@dispatcher.message(Form.feeder, lambda message: not laying_provided(message.text) and load_provided(message.text))
async def process_laying(message: Message, state: FSMContext) -> None:
    await state.update_data(feeder=message.text)
    await state.set_state(Form.laying)
    await message.answer("Wählen Sie bitte den Verlegeart des Kabels.\nVerwenden Sie bitte die Schaltflächen unten:",
                         reply_markup=ReplyKeyboardMarkup(keyboard=keyboard_laying().export(), resize_keyboard=True)),


@dispatcher.message(F.text.casefold().in_({'/hv', 'hv'}))
@dispatcher.message(Form.laying, lambda message: laying_provided(message.text, find_ref=True))
@dispatcher.message(Form.feeder, lambda message: laying_provided(message.text) and load_provided(message.text))
async def process_feeder(message: Message, state: FSMContext) -> None:
    try:
        user_input = (await state.get_data())["feeder"]
        laying_from_keyboard = laying_provided(message.text, just_match=False)
        feeder = f'{user_input}{laying_from_keyboard}'
    except KeyError:
        feeder = message.text
    if feeder not in ["hv", "/hv"]:
        preliminary_data = parse_input(feeder)
        preliminary_name = get_name(preliminary_data)
        await message.answer(f'Abgang  <i>{preliminary_name}</i> \nerfolgreich zu Liste hinzugefügt')
        await update_feeder(data=preliminary_data, set_exactly=False)
    await state.clear()
    await state.set_state(Form.feeder)
    await message.answer(
        "Geben Sie die Daten des Stromkreises ein.\n"
        "<i>Beispiel: UV-AV-EG 23kw 56m</i>",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Fertig"),
                    KeyboardButton(text="Abbruch")
                ]
            ],
            resize_keyboard=True,
        ),
        parse_mode="HTML"
    )


@dispatcher.message(Form.project)
async def process_result(message: Message, state: FSMContext):
    await state.clear()
    project_number, project_name, switchboard = parse_project(message.text)
    await state.set_data({'project_number': project_number,
                          'project_name': project_name,
                          'switchboard': switchboard})
    data = await state.get_data()
    try:
        await update_feeder(data, set_exactly=False)
    except TypeError:
        pass
    await message.answer(f"Fertig! Unten ist das NSHV-Schema und\n"
                         f"die NSHV-Berechnung für das Projekt\n"
                         f"{project_number} {project_name}",
                         reply_markup=ReplyKeyboardRemove())
    dxf_path, pdf_path = summary(project_data)
    filename = f"{project_number} {project_name}, {switchboard}"
    await message.answer_document(FSInputFile(dxf_path, filename=f"{filename}.dxf"))
    await message.answer_document(FSInputFile(pdf_path, filename=f"{filename}.pdf"))


@dispatcher.message(Form.laying)
@dispatcher.message(Form.feeder)
@dispatcher.message(lambda message: not re.search(r'kw|a', message.text.casefold()))
async def process_error(message: Message) -> None:
    await message.answer('Überprüfen Sie bitte die Richtigkeit Ihrer Angaben. '
                         'Probieren Sie es noch mal:', reply_markup=ReplyKeyboardRemove())


async def update_feeder(data: [list, Any], set_exactly: bool) -> None:
    if set_exactly:
        project_data[0] = data
    else:
        project_data.append(data)


@dispatcher.message(state=None)
async def process_message(message: Message):
    try:
        parsed_data = parse_input(message.text)
        computed_data = calc(parsed_data)
        fdata = format_values(computed_data)
        name, power, g, phi, voltage, cable, section, length, du, laying_simple, cb, cb_type, release, ib = fdata
        await message.answer(f'<code>Verteiler:     {name}\n'
                             f'Leistung:      {power}\n'
                             f'Gleichz.-keit: {g}\n'
                             f'cos(f):        {phi}\n'
                             f'Spannung:      {voltage}\n'
                             f'Kabel:         {cable}\n'
                             f'Querschnitt:   {section}\n'
                             f'Kabellänge:    {length}\n'
                             f'Spannungsfall: {du}\n'
                             f'Verlegeart:    {laying_simple}\n'
                             f'Schutzorgan:   {cb}\n'
                             f'S.-organ Typ:  {cb_type}\n'
                             f'Auslöser:      {release}\n'
                             f'Ausl.-strom:   {ib}</code>',
                             parse_mode='HTML')

    except (TypeError, ValueError):
        await message.reply('Ein Fehler ist aufgetreten. Überprüfen Sie bitte die Richtigkeit Ihrer Angaben.')


if __name__ == "__main__":
    asyncio.run(dispatcher.start_polling(Bot(token=TOKEN, parse_mode="HTML")))
