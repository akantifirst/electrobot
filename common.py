import re
import csv
from datetime import (
    date,
    datetime)

from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config import (
    LAYING,
    LAYING_TYPES)


def csv_read(path: str) -> list:
    """
        Write csv content to nested list
    """
    data = []
    for row in csv.reader(open(f'{path}', 'r', encoding="utf-8"), delimiter=';'):
        data.append(row)
    return data


def load_provided(message_text: str):
    """
        Checks if electrical load is provided in user message
        "23kw", "23a" -> load provided;
        "kw", "a", "23 kw", "23 a", "foo" -> load not provided;
    """
    message_text = message_text.lower()
    load_pattern = r'[0-9]kw |[0-9]kw$|[0-9]a$|[0-9]a '
    return re.search(load_pattern, message_text)


def convert_ref(message_text: str) -> str:
    """
        Converts long laying type description to laying type reference
        according to table in LAYING.csv. Example:
        "Installationskanal" -> "e1"
    """
    laying_table = csv_read(r'db/LAYING.csv')
    try:
        index = [row[1] for row in laying_table].index(message_text)
        ref_laying = str(laying_table[index][0])
    except ValueError:
        ref_laying = LAYING
    return ref_laying


def laying_provided(message_text: str, find_ref=False, just_match=True):

    """
        Checks if laying type reference is provided in user message
        "23kw a1", find_ref=False -> laying provided;
        "23kw" -> laying not provided
        "In Erde", find_ref=True -> laying provided;
        "In Erde", find_ref=False -> laying not provided; fallback to default

        Parameters:
        message_text: keyboard input e.g. "Installationskanal" or text input e.g. "23kw a1"
        find_ref: whether to convert message to reference or not
        just_match: whether to return matched laying type or return just match
    """
    laying_types = LAYING_TYPES

    # If we need to convert short description to laying type reference
    if find_ref:
        ref_laying = convert_ref(message_text)
    else:
        ref_laying = re.search(laying_types, message_text.lower())
        if ref_laying:
            ref_laying = ref_laying.group(0)[1:]

    # Whether to return string value or match
    if just_match:
        return re.match(laying_types, f' {ref_laying}')
    else:
        return f' {ref_laying}'


def get_name(preliminary_data: list) -> str:
    """
    Get switchboard name and load.
    This is simplified preliminary parsing without validation/calculation.
    Is used to display a message that the feeder is succesfully added.
    """
    # Normally, switchboard name must be uppercase
    pre_name = preliminary_data[0].upper()

    # Error handling if commas in user input
    pre_power = str(preliminary_data[1]).replace(',', '.')
    pre_current = str(preliminary_data[2]).replace(',', '.')

    # Load can be current or power, depends on user input
    pre_load = f"P={pre_power}kW" if preliminary_data[1] != " " else f"I={pre_current}A"
    return f'{pre_name} {pre_load}'


def keyboard_laying() -> ReplyKeyboardBuilder:
    """
        Generates telegram bot reply keyboard.
        Button texts=values are taken from LAYING.csv
    """
    # Aiogram v3 provides special keyboard builder
    kb_laying = ReplyKeyboardBuilder()
    laying_table = csv_read(r'db/LAYING.csv')

    # Generate keyboard buttons
    for element in [row[1] for row in laying_table]:
        kb_laying.add(KeyboardButton(text=f'{element}'))

    # Align buttons in one column
    kb_laying.adjust(1)
    return kb_laying


def get_datetime():
    """
        Self-explained function
    """
    now = datetime.now().strftime("%H:%M")
    today = date.today().strftime("%d.%m.%y")
    return now, today
