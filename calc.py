import math
from contextlib import suppress


def clear_chars(input_string):
    """This function deletes all chars from the string,
    except digits or decimal separation dot"""
    # Split string first, add symbols to new list if they match the condition.
    # Finally concatenate all symbols to string.
    number = float(''.join([e for e in input_string if e.isdigit() or e == '.']))
    return number


def calc(message):
    """This function calculates electrical power in kW
    or electrical current in A"""
    # Where the user request is processed.
    power, current, voltage, power_factor = parse_input(message)
    # Not sure if user wants power or current
    try:
        power = (math.sqrt(3) * power_factor * voltage * current) / 1000
    except TypeError:
        # If this happens, {current} variable still equals whitespace and cant be divided
        # It means, that user entered power and expects current to be calculated
        current = 1000 * power / (math.sqrt(3) * power_factor * voltage)
    return power, current, voltage, power_factor


def parse_input(user_input):
    """This function parses user input and finds the values of
    electrical current, power, power factor or voltage"""
    # These are default values
    power, current, voltage, power_factor = ' ', ' ', 400, 0.95
    # Refine user input
    print(user_input)
    data = user_input.replace(',', '.').lower().split(' ')
    # First check if user provided suffices to values
    try:
        for e in data:
            if any([x in e for x in ['a', 'а']]):
                current = clear_chars(e)
            elif any([x in e for x in ['kw', 'кв']]):
                power = clear_chars(e)
            elif any([x in e for x in ['v', 'в']]):
                voltage = clear_chars(e)
            else:
                # If suffices are missing, try to guess what user means
                with suppress(IndexError):
                    # Check if first element of input is a number
                    if not data[0].islower():
                        power = float(data[0])
                    if 0.5 <= float(e) <= 1:
                        power_factor = float(e)
                    # If no suffix vor voltage specifies, choose between 230V and 400V
                    if e in {'230', '400'}:
                        voltage = float(e)
        return power, current, voltage, power_factor
    except ValueError:
        print('Please review your request')
