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