import math
from contextlib import suppress


def clear_chars(input_string):
    """This function deletes all chars from the string,
    except digits or decimal separation dot"""
    # Split string first, add symbols to new list if they match the condition.
    # Finally concatenate all symbols to string.
    number = float(''.join([e for e in input_string if e.isdigit() or e == '.']))
    return number


def calc():
    """This function calculates electrical power in kW
    or electrical current in A"""
    # Where the user request is processed.
    power, current, voltage, power_factor = parse_input(input('Enter the values: '))
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
    data = user_input.replace(',', '.').lower().split(' ')
    # First check if user provided suffices to values
    for e in data:
        if 'a' in e:
            current = clear_chars(e)
        elif 'kw' in e:
            power = clear_chars(e)
        elif 'v' in e:
            voltage = clear_chars(e)
        else:
            # If suffices are missing, try to guess what user means
            with suppress(IndexError):
                #
                if not data[0].islower():
                    power = float(data[0])
                if 0.5 <= float(e) <= 1:
                    power_factor = float(e)
                if e in {'230', '400'}:
                    voltage = float(e)

    return power, current, voltage, power_factor


def main():
    """This is the main function"""
    print('Welcome to power/current calc. '
          'Please enter either current (add A) or power (add kW),'
          'and optionally voltage and power factor. ')

    power, current, voltage, power_factor = calc()

    print(f'Power is {power:.2f}kW, '
          f'Current is {current:.2f}A, '
          f'Voltage is {voltage:.0f}V, '
          f'Power factor is {power_factor:.2f}')


main()
