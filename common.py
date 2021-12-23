from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import csv


def csv_read(path: str) -> list:
    data = []
    for row in csv.reader(open(f'{path}', 'r', encoding="utf-8"), delimiter=';'):
        data.append(row)
    return data


def convert_laying(short_descr: str) -> str:
    data = csv_read(r'db/LAYING.csv')
    try:
        index = [e[1] for e in data].index(short_descr)
        return data[index][0]
    except ValueError:
        return 'e1'


def keyboard_laying():
    kb_laying = ReplyKeyboardBuilder()
    data = csv_read(r'db/LAYING.csv')
    for e in [e[1] for e in data]:
        kb_laying.add(KeyboardButton(text=f'{e}'))
    kb_laying.adjust(1)
    return kb_laying
