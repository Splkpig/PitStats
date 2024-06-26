import re

import discord


def add_commas(number):
    return "{:,}".format(number)


def int_to_roman(num):
    if num == 0:
        return ""

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
    return roman_num + "-"


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


def format_playtime(playtime_minutes):
    # Constants for time conversion
    MINUTES_IN_HOUR = 60
    HOURS_IN_DAY = 24
    DAYS_IN_MONTH = 30

    # Convert minutes to hours
    total_hours = playtime_minutes / MINUTES_IN_HOUR

    # Format playtime based on total hours
    if total_hours < HOURS_IN_DAY:
        return f"{total_hours:.0f} hr"
    elif total_hours < HOURS_IN_DAY * DAYS_IN_MONTH:
        days = int(total_hours // HOURS_IN_DAY)
        hours = total_hours % HOURS_IN_DAY
        return f"{days} d, {hours:.0f} hr"
    else:
        total_days = total_hours / HOURS_IN_DAY
        months = int(total_days // DAYS_IN_MONTH)
        days = total_days % DAYS_IN_MONTH
        return f"{months} mo, {days:.0f} d"


def extract_name(input_string):
    # Find the position of the last instance of '§b'
    last_index = input_string.rfind(' ')

    if last_index != -1:
        # Extract the substring after the last '§b'
        name = input_string[last_index + 3:]
        return name
    else:
        return None


def formatRankingsData(listToFormat):
    blackListed = ['damageRatio', 'highestStreak', 'kdr', 'tierOnes', 'tierTwos', 'darkPantsT2', 'totalJumps', 'bounty', 'genesisPoints', 'joins', 'bowAccuracy', 'swordHits', 'meleeDamageDealt', 'meleeDamageReceived', 'meleeDamageRatio', 'bowDamageDealt', 'bowDamageReceived', 'bowDamageRatio', 'xpHourly', 'goldHourly', 'killsHourly', 'kadr', 'killAssistHourly', 'contractsStarted', 'contractsRatio', 'ingotsGold']

    return [value if key in blackListed else (value if isinstance(value, (int, float)) else 999999) for key, value in listToFormat.items() if key not in blackListed]


def leaderboardEmbed(players, embed, page):
    i = 1
    for player in players:
        if player == 'Splkpig':
            player = f'<:splkpig:1172711478223188068> {player}'
        elif player == 'Reyertic':
            player = f'<:reyerticicon:1197414722564276335> {player}'

        embed.add_field(name=f"#{page * 10 + i}:", value=f"{player}", inline=False)
        i += 1
    return embed


def leaderboardEmbedAll(players, embed):
    i = 1
    for player in players:
        if player == 'Splkpig':
            player = f'<:splkpig:1172711478223188068> {player}'
        elif player == 'Reyertic':
            player = f'<:reyerticicon:1197414722564276335> {player}'

        embed.add_field(name=f"#{i}:", value=f"{player}", inline=False)
        i += 1
    return embed
