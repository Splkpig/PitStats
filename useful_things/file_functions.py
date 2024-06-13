import time


def read_specific_line(file_path, line_number):
    """
    Reads a specific line from a text file.

    :param file_path: Path to the text file
    :param line_number: The line number to read (1-based index)
    :return: The content of the specified line or None if the line does not exist
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Convert line_number to 0-based index
            index = line_number
            if 0 <= index < len(lines):
                return lines[index].strip()  # Use strip() to remove any trailing newline characters
            else:
                return None
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def startSession(player, userID, xp, gold, kills, deaths, playtime):
    timeUNIX = int(time.time())
    stats_string = f"{player}:{userID}:{xp}:{gold}:{kills}:{deaths}:{playtime}:{timeUNIX}"

    with open("../PitStats/storage/sessions.txt", "a") as file:
        file.write(stats_string + '\n')


def viewSession(userID):
    with open("../PitStats/storage/sessions.txt", "r") as file:
        for line in file:
            fromFileID = line.split(":", 2)[1]
            if str(userID) == fromFileID:
                return line
    return None


def endSession(userID):
    with open("../PitStats/storage/sessions.txt", "r") as file:
        lines = file.readlines()

    updated_lines = [line for line in lines if not line.split(":")[1] == str(userID)]
    with open("../PitStats/storage/sessions.txt", "w") as file:
        file.writelines(updated_lines)


def hasSession(userID):
    with open("../PitStats/storage/sessions.txt", "r") as file:
        for line in file:
            fromFileID = line.split(":", 2)[1]
            if str(userID) == fromFileID:
                return True
    return False


def checkSessions():
    with open("../PitStats/storage/sessions.txt", "r") as file:
        for line in file:
            fromFileTime = int(line.split(":")[7])
            if fromFileTime + 86400 <= int(time.time()):
                # print(f"Ended session for: {line.split(':')[0]}")
                endSession(line.split(":")[1])