import re


def add_commas(number):
    return "{:,}".format(number)


def int_to_roman(num):
    if not (1 <= num <= 50):
        raise ValueError("Number out of range, must be between 1 and 50")

    val = [
        50, 40, 10, 9, 5, 4, 1
    ]
    syb = [
        "L", "XL", "X", "IX", "V", "IV", "I"
    ]

    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num


def extract_number(input_string):
    # Define the regular expression pattern to match numbers
    pattern = r'\d+'

    # Search the pattern in the input string
    match = re.search(pattern, input_string)

    # If a match is found, return the matched number
    if match:
        return match.group(0)
    else:
        return None


def extract_substring(input_string):
    # Find the position of the hyphen
    hyphen_pos = input_string.find('-')

    if hyphen_pos == -1:
        return None  # Hyphen not found

    # Calculate the starting position (4 characters after the hyphen)
    start_pos = hyphen_pos + 5

    # Ensure start_pos is within the string length
    if start_pos >= len(input_string):
        return None

    # Find the position of the next '§' after the starting position
    end_pos = input_string.find('§', start_pos)

    if end_pos == -1:
        return None  # Next '§' not found

    # Extract the substring from start_pos to end_pos
    result = input_string[start_pos:end_pos]

    return result