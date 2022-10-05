"""
    Program:  Chapter 5 Project 2
    Author:   Jeff Alkire
    Date:     October 4, 2021
"""
from os.path import exists

def get_filename_from_user() -> str:
    """
    Get a filename from the user and verify it exists.  If not, keep asking.
    :return: the name of the existing file as supplied by the user
    """
    filename = ""
    while filename == "":
        filename = input("Name of file: ")
        if not exists(filename):
            print("   *** FILE NOT FOUND ***")
            filename = ""
    return filename


def file_to_lines(filename: str) -> [str]:
    """
    Read the given filename splitting the results by line.

    :param      filename: name of the file to read
    :return:    a list of strings with each list entry containing a single
                    line from the file.
    """
    print(filename)
    with open(filename) as f:
        results = f.readlines()
    return results

def prompt_user(file_lines: [str]) -> int:
    """
    Display instruction to the user.

    :param file_lines:  list of lines from the file.
    """
    print("There are %d lines in the file." % len(file_lines))
    print("    Enter 0 to exit or a line number to exit:", end=" ")
    result_str = input()
    return int(result_str)

def verify_entry_range(line_num: int, file_lines: [str]) -> bool:
    """
    Is the supplied line number within the range of valid line #s?
    :param line_num:   the line # chosen by user
    :param file_lines: the lines from the file
    :return:  True if the supplied line_num is valid, False if not.
    """
    return (line_num >= 0  and  line_num <= len(file_lines))

def invalid_entry_message(line_num: int, file_lines: [str]) -> None:
    """
    Inform user of their mistake and ask again.
    :param line_num:   the line # chosen by user
    :param file_lines: the lines from the file
    """
    print("%d is an INVALID entry." % line_num)
    print("    Entry must be between 0 and %d." % len(file_lines))
    print("    PLEASE TRY AGAIN.")
    print()

def get_line_number_from_user(file_lines: [str]) -> int:
    """
    Ask the user for a line number
    :param file_lines:
    :return:
    """
    line_num = prompt_user(file_lines)
    if verify_entry_range(line_num, file_lines):
        return line_num
    else:
        invalid_entry_message(line_num,file_lines)
        return get_line_number_from_user(file_lines)

def display_line(line_num: int, file_lines: [str]) -> None:
    """
    Display the specified line from lines in the file
    :param line_num:     line number to display
    :param file_lines:   all lines from file.
    """
    print("Line # %d is:" % line_num)
    print("   " + file_lines[line_num-1])

def loop_until_zero(file_lines: [str]) -> None:
    """
    Loop until the user supplies a 0 as the line number
    :param file_lines:  list of lines from the user supplied file.
    """
    while True:
        line_num_as_str = get_line_number_from_user(file_lines)
        line_num = int(line_num_as_str)

        if line_num == 0:
            return
        elif verify_entry_range(line_num,file_lines):
            display_line(line_num,file_lines)
        else:
            invalid_entry_message(line_num, file_lines)

def main():
    filename = get_filename_from_user()
    file_lines = file_to_lines(filename)
    loop_until_zero(file_lines)

if __name__ == "__main__":
    main()