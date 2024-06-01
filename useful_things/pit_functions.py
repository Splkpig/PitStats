from useful_things.file_functions import read_specific_line


def calcBracketColor(prestige: int):
    if prestige == 0:
        return 0xAAAAAA
    elif int(prestige / 5) == 0:
        return 0x5555FF
    elif int(prestige / 5) == 1:
        return 0xFFFF55
    elif int(prestige / 5) == 2:
        return 0xFFAA00
    elif int(prestige / 5) == 3:
        return 0xFF5555
    elif int(prestige / 5) == 4:
        return 0xAA00AA
    elif int(prestige / 5) == 5:
        return 0xFF55FF
    elif int(prestige / 5) == 6:
        return 0xffffff
    elif int(prestige / 5) == 7:
        return 0x55FFFF
    elif int(prestige / 5) == 8:
        return 0x0000AA
    elif prestige == 45 or prestige == 46 or prestige == 47:
        return 0x000000
    elif prestige == 48 or prestige == 49:
        return 0xAA0000
    else:
        return 0x555555


def calculateXPForLevel(prestige: int, level: int):
    prestigeMultiplier = float(read_specific_line("../PitStats/useful_things/pitdata/xp_multipliers.txt", prestige))
    levelTensChunk = int(level / 10)
    levelsAfterTen = level - (levelTensChunk * 10)

    totalXP = 0
    for i in range(0, levelTensChunk):
        totalXP += (prestigeMultiplier * int(
            read_specific_line("../PitStats/useful_things/pitdata/base_level_xp.txt", i))) * 10

    totalXP += (prestigeMultiplier * int(
        read_specific_line("../PitStats/useful_things/pitdata/base_level_xp.txt", levelTensChunk))) * levelsAfterTen

    return totalXP


def xpToLevel(prestige: int, xp: int):
    prestigeMultiplier = float(read_specific_line("../PitStats/useful_things/pitdata/xp_multipliers.txt", prestige))
    xpOfPrestige: int = 0

    for i in range(0, 13):
        for j in range(0, 10):
            xpOfPrestige += int(
                read_specific_line("../PitStats/useful_things/pitdata/base_level_xp.txt", i)) * prestigeMultiplier
            if xpOfPrestige > xp:
                return i * 10 + j
    return 120


def calculateFactionTier(points: int):
    pointsBreakdown = [30, 100, 250, 700, 1500, 4000, 7000]

    for pointCategory in pointsBreakdown:
        if pointCategory > points:
            return pointsBreakdown.index(pointCategory)

    return 7
