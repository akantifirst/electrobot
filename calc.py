import csv
from math import sqrt, sin, acos
import random
import string


def clear_chars(input_string):
    """This function deletes all chars from the string,
    except digits or decimal separation dot"""
    # Split string first, add symbols to new list if they match the condition.
    # Finally concatenate all symbols to string.
    number = float(''.join([e for e in input_string if e.isdigit() or e == '.']))
    return number


def parse_input(user_input):
    """
    This function parses user input and finds the values of
    electrical current, power, power factor or voltage
    input:
    uv-av-o1 35kw 380 0.98 d1 nycwy 56m	*alu *1.OGg *abb
    output:
    [ name,      P,  I,    U,   phi,  laying, cable, length, medium, floor,  maker, du_max]
	["uv-av-eg", 35, None, 400, 0.95, "c1",   "nyy", 120,    "alu",  "1.og", "abb", 2.5]
	"""
    e = "All good!"  # for debugging
    # These are default values todo move to config
    name = 'UV-AV-XX'
    power = ' '
    current = ' '
    voltage = 400
    phi = 0.95
    laying = "e1"
    cable = "nyy"
    length = 30
    medium = "cu"
    floor = ' '
    maker = "abb"
    du_max = 1.5

    # Refine user input
    data = user_input.replace(',', '.').lower().split(' ')
    # get name
    if sum(c.isalpha() for c in data[0]) > 2 or sum(c.isdigit() for c in data[0]) == 0:
        name = data[0]
        data = data[1:]

    try:
        for e in data:
            if e[len(e) - 1] == 'a':
                current = clear_chars(e)  # get current
            elif any([x in e for x in ['kw']]):
                power = clear_chars(e)  # get power
            elif any([x in e for x in ['nyy', 'nym', 'nycwy', 'nhxh']]):
                cable = str(e)  # get cable
            elif any([x in e for x in ['v']]):
                voltage = clear_chars(e)  # get voltage
            elif any([x in e for x in ['m']]):
                length = clear_chars(e)  # get length
            elif any([x in e for x in ['a1', 'a2', 'b1', 'b2', 'c1', 'd1', 'e1', 'f1', 'f2', 'f3', 'g1', 'g2']]):
                laying = str(e)  # get laying
            elif any([x in e for x in ['alu', 'cu']]):
                medium = str(e)  # get medium
            elif e[len(e) - 1] == 'g':
                floor = str(e)[:-1]  # get floor
            elif any([x in e for x in ['abb', 'siemens', 'hager']]):
                maker = str(e)  # get maker
            elif e[len(e) - 1] == '%':
                du_max = float(e[:-1])  # get du_max
            elif 0.6 <= float(e) <= 1.0:
                phi = float(e)

        parsed_data = [name, power, current, voltage, phi, laying, cable, length, medium, floor, maker, du_max]
        return parsed_data
    except ValueError:
        print(f'Please review your request: {e} [parse_input]')


# parse_input("uv-av-o1 24kw 380 0.98 g1 nycwy 56m alu abb 1,5%")


def power_current(power, current, voltage, phi):
    """This function calculates electrical power in kW
        or electrical current in A"""
    # Not sure if user wants power or current
    try:
        if voltage >= 300:
            power = round((sqrt(3) * phi * voltage * current) / 1000, 2)
        else:
            power = round((phi * voltage * current) / 1000, 2)
    except TypeError:
        # If this happens, {current} variable still equals whitespace and cant be divided
        # It means, that user entered power and expects current to be calculated
        if voltage >= 300:
            current = round(1000 * power / (sqrt(3) * phi * voltage), 2)
        else:
            current = round(1000 * power / (phi * voltage), 2)
    return power, current


def cable_section(voltage, length, current, phi, medium, laying, du_max):
    """
    Finds in table the minimal cable section allowed for this current and kind of laying
    """
    data, section_ib, section_du, system_ib, system_du, system = [], '?', '?', 1, 1, 1
    laying = laying + '.3' if voltage >= 370 else laying + '.2'
    for row in csv.reader(open(r'/nb_electrobot/CU_Z70_U30.csv', 'r'), delimiter=';'):
        data.append(row)
    # find the right column based on the way of laying:
    index_laying = data[0].index(laying)
    current_list = [e[index_laying] for e in data][1:]
    section_list = [e[0] for e in data][1:]
    # check current condition:
    for system_ib in range(1, 8):
        try:
            section_ib = next(data[i + 1][0] for i, v in enumerate(current_list) if float(v) >= current / system_ib)
            break
        except (ValueError, IndexError):
            print(r'Cant find cable section - check index or value')
        except StopIteration:
            continue
    # check du condition
    ro = 0.0225 if medium == 'cu' else 0.036
    x = 0.08
    for system_du in range(1, 4):
        try:
            section_du = (ro * length * phi) / \
                 ((voltage * du_max / (sqrt(3) * (current/system_du) * 100)) - (x * length * sin(acos(phi)) / 1000))
            section_du = next(v for v in section_list if float(v) >= section_du)
            break
        except StopIteration:
            continue
    try:
        if float(section_ib*system_ib) > float(section_du*system_du):
            section = float(section_ib)
            system = system_ib
        else:
            section = float(section_du)
            system = system_du

        du = round(100 * (sqrt(3) * ((ro * length * phi) / float(section) +
                                     (x * length * sin(acos(phi))) / 1000) * (current/system)) / voltage, 2)
    except ValueError:
        section, du = '?', '?'
    return section, system, du


def circuit_breaker(current):
    data = []
    for row in csv.reader(open(r'/nb_electrobot/CB.csv', 'r'), delimiter=';'):
        data.append(row)
    cb_currents = [e[0] for e in data[1:]]
    cb_current = next(v for v in cb_currents if float(v) >= current)
    current = "LS-Schalter " + str(cb_current) + "A"
    return current


def calc(parsed_data):
    # Where the user request is processed.
    name, power, current, voltage, phi, laying, cable, length, medium, floor, maker, du_max = parsed_data
    # calculate power and current
    power, current = power_current(power, current, voltage, phi)
    # now that we have current we can calculate the cable section
    section, system, du = cable_section(voltage, length, current, phi, medium, laying, du_max)

    cb = circuit_breaker(current)
    computed_data = [name, power, current, voltage, phi, laying,
                     cable, length, medium, floor, maker, section, system, du, cb]
    return computed_data


# calc(['uv-av-o1', 300.0, ' ', 400, 0.98, 'c1', 'nycwy', 56.0, 'alu', '1.og', 'abb', 1.5])


def format_values(feeder):
    """
    This function formats all computed values for human interaction
    either in form of a pdf file or by message in Telegram
    """
    poles = "5" if feeder[3] > 240 else "3"
    system = str(feeder[12]) + "x" if feeder[12] > 1 else ''
    feeder[0] = feeder[0].upper()
    # feeder power
    feeder[1] = (f'{float(feeder[1]):.1f}' + "kW").replace('.', ',')
    # feeder current
    feeder[2] = (f'{float(feeder[2]):.1f}' + "A").replace('.', ',')
    # feeder voltage
    feeder[3] = f'{float(feeder[3]):.0f}' + "V"
    # feeder phi
    feeder[4] = str(feeder[4]).replace('.', ',')
    # feeder_laying
    try:
        data = []
        for row in csv.reader(open(r'/nb_electrobot/LAYING.csv', 'r', encoding='utf8'), delimiter=';'):
            data.append(row)
        tdata = list(zip(*data))
        # find the right column based on the way of laying:
        index_laying = list(tdata[0]).index(feeder[5][:2].lower())
        feeder[5] = list(tdata[1])[index_laying]
    except (TypeError, ValueError):
        print('Please review your request [format_values.laying]')
    # feeder cable
    feeder[6] = feeder[6].upper()
    # feeder length
    feeder[7] = f'{float(feeder[7]):.0f}' + "m"
    # feeder medium
    feeder[8] = feeder[8].capitalize()
    # feeder floor
    feeder[9] = feeder[9].upper()
    # feeder maker
    feeder[10] = feeder[10].upper()
    # feeder section
    feeder[11] = system + (poles + "x" + str(feeder[11]).rstrip('0').rstrip('.')).replace('.', ',') + "mm²"

    # feeder voltage drop
    feeder[13] = (str(feeder[13]) + "%").replace('.', ',')
    # feeder circuit breaker
    feeder[14] = feeder[14].replace('.', ',')
    return feeder
