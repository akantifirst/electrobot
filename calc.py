import re
from math import sqrt, sin, acos
from export import generate_pdf
from cad import cad_write
from common import csv_read
from config import *


# BUG: du has no effect with bigger power e.g. 500kw 300m


def clear_chars(input_string):
    """This function deletes all chars from the string,
    except digits or decimal separation dot"""
    number = float(''.join([e for e in input_string if e.isdigit() or e == '.']))
    return number


def parse_input(user_input):
    """
    This function parses user input and finds the values of
    electrical current, power, power factor or voltage
    """

    name = NAME
    power = POWER
    current = CURRENT
    voltage = VOLTAGE
    phi = PHI
    laying = LAYING
    cable = CABLE
    length = LENGTH
    medium = MEDIUM
    g = G
    maker = MAKER
    du_max = DU_MAX

    # Refine user input
    user_input = re.sub(' +', ' ', user_input).replace(',', '.').lower().split(' ')
    # get name of feeder
    if sum(c.isalpha() for c in user_input[0]) > 2 or sum(c.isdigit() for c in user_input[0]) == 0:
        name = user_input[0]
        user_input = user_input[1:]
    try:
        for word in user_input:
            if word[len(word) - 1] == 'a':
                current = clear_chars(word)  # get current
            elif any([_ in word for _ in ['kw']]):
                power = clear_chars(word)  # get power
            elif any([_ in word for _ in ['nyy', 'nym', 'nycwy', 'nhxh']]):
                cable = str(word)  # get cable
            elif word[len(word) - 1] == 'v':
                voltage = clear_chars(word)  # get voltage
            elif word[len(word) - 1] == 'm':
                length = clear_chars(word)  # get length
            elif any([_ in word for _ in ['a1', 'a2', 'b1', 'b2', 'c1', 'd1', 'e1', 'f1', 'f2', 'f3', 'g1', 'g2']]):
                laying = str(word)  # get laying
            elif any([_ in word for _ in ['alu', 'cu']]):
                medium = str(word)  # get medium
            elif word[len(word) - 1] == 'g':
                g = float(word[:-1])  # get g (german: gleichzeitigkeitsfaktor)
            elif any([_ in word for _ in ['abb', 'siemens', 'hager']]):
                maker = str(word)  # get maker
            elif word[len(word) - 1] == '%':
                du_max = float(word[:-1])  # get du_max
            elif not re.search('[a-zA-Z]', word) and 0.6 <= float(word) <= 1.0:
                phi = float(word)

        # Correct user input. F1 laying type is onle for 1-pole feeders
        if voltage >= 300 and laying == 'f1':
            laying = 'f2'
        parsed_data = [name, power, current, voltage, phi, laying, cable, length, medium, g, maker, du_max]
        return parsed_data
    except ValueError:
        print(f'Überpüfen sie bitte die Richtigkeit ihrer Angaben.')


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
    data = csv_read(r'db/CU_Z70_U30.csv')
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
            print(r'Kann den Kabelquerschnitt nicht berechnen - überprüfen sie bitte den Index oder den Wert.')
        except StopIteration:
            continue
    # check du condition
    ro = RO_CU if medium == 'cu' else RO_AL
    x = X
    for system_du in range(1, 8):
        try:
            section_du = (ro * length * phi) / \
                         ((voltage * du_max / (sqrt(3) * (current / system_du) * 100)) - (
                                 x * length * sin(acos(phi)) / 1000))
            section_du = next(v for v in section_list if float(v) >= section_du)
            break
        except StopIteration:
            continue
    # choose max from ib and du conditions
    try:
        if float(section_ib * system_ib) > float(section_du * system_du):
            section = float(section_ib)
            system = system_ib
        else:
            section = float(section_du)
            system = system_du
        du = round(100 * (sqrt(3) * ((ro * length * phi) / float(section) +
                                     (x * length * sin(acos(phi))) / 1000) * (current / system)) / voltage, 2)
    except ValueError:
        section, du = '?', '?'
    return section, system, du


def circuit_breaker(current, maker, voltage):
    """
    Finds circuit breaker and tripping unit
    """
    db = f'db/{maker.upper()}.csv'
    poles = "3" if voltage > 240 or current > 63 else "1"
    data = csv_read(db)

    # feeder cb (circuit breaker)
    cb = f'LS-Schalter {poles}P'
    # feeder circuit breaker type and release type
    if current < 63:
        release = "-"
        if poles == "3":
            cb_type = next(v[2] for v in data if float(v[0]) >= current)
        else:
            cb_type = next(v[1] for v in data if float(v[0]) >= current)
    else:
        cb_type = next(v[1] for v in data if float(v[0]) >= current)
        release = next(v[2] for v in data if float(v[0]) >= current)

    # feeder ib (german: betriebsstrom)
    ib = ("Ir=" + f'{float(current):.1f}' + "A").replace('.', ',')
    return cb, cb_type, release, ib


def calc(parsed_data):
    """
    Main function that gathers all other subfunctions
    """
    name, power, current, voltage, phi, laying, cable, length, medium, g, maker, du_max = parsed_data
    # calculate power and current
    power, current = power_current(power, current, voltage, phi)
    # now that we have current we can calculate the cable section
    section, system, du = cable_section(voltage, length, current, phi, medium, laying, du_max)
    # select circuit breaker
    cb, cb_type, release, ib = circuit_breaker(current, maker, voltage)
    computed_data = [name, power, current, voltage, phi, laying,
                     cable, length, medium, g, maker, section, system, du, cb, cb_type, release, ib]
    return computed_data


def format_values(computed_data):
    """
    This function formats computed_data for export in CAD and bot answer
    """
    name, power, current, voltage, phi, laying, cable, length, medium, g, \
        maker, section, system, du, cb, cb_type, release, ib = computed_data

    poles = "5" if voltage > 240 else "3"
    ref_laying = "3" if voltage > 240 else "2"

    system = str(system) + "x" if system > 1 else ''
    name = name.upper()
    power = ("P=" + f'{float(power):.1f}' + "kW").replace('.', ',')
    g = 'g=' + str(g).replace('.', ',')
    phi = "cos(f)=" + str(phi).replace('.', ',')
    voltage = "U=" + f'{float(voltage):.0f}' + "V"
    cable = f'{cable.upper()}({medium.capitalize()})'
    section = system + (poles + "x" + str(section).rstrip('0').rstrip('.')).replace('.', ',') + "mm²"
    length = "L=" + f'{float(length):.0f}' + "m"
    du = "dU=" + (str(du).replace('.', ',')) + "%"
    laying = f'{laying.upper()}.{ref_laying}'

    formatted_data = [name, power, g, phi, voltage, cable, section,
                      length, du, laying, cb, cb_type, release, ib]
    return formatted_data


def summary(data):
    fdata, power_inp, project_info = [], 0, data[-1]
    pdf_path, dxf_path = PDF_LOCATION, DXF_LOCATION

    # Perform calculations and formatting sequentially to each feeder
    for feeder in data[:-1]:
        computed_data = calc(feeder)
        fdata.append(format_values(computed_data))
        power_inp += round(computed_data[1] * computed_data[9], 2)

    # Calculate cumulative power for the power input
    if len(data[:-1]) < 3:
        power_inp = calc(data[0])[1] * 1.6
    power_inp = f"{power_inp}kW e1"
    fdata.append(format_values(calc(parse_input(power_inp))))

    # Functions for generating .dxf and .pdf files
    cad_write(fdata, project_info)
    generate_pdf(dxf_path, pdf_path)

    # Clear data structures for the current user request
    data.clear()
    fdata.clear()
    return dxf_path, pdf_path


def parse_project(data: str):
    project_number = "10xx"
    project_name = "Projekt Name"
    switchboard = "NSHV/GHV"
    if "," in data:
        switchboard = data.split(", ")[1]
        project_info = data.split(", ")[0]
    else:
        project_info = data
    if " " in project_info:
        if sum(_.isalpha() for _ in project_info[0]) == 0:
            project_number = project_info.split(" ")[0]
        project_name = " ".join(project_info.split(" ")[1:])
    else:
        if sum(_.isalpha() for _ in project_info) == 0:
            project_number = project_info
    return project_number, project_name, switchboard
