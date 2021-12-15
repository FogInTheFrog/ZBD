# Functions responsible for csv analysis
from time import sleep
from typing import List, Tuple


# Splits line when combination of quotes_type and
# separator occur, without removing quotes
def split_line(line: str, separator: str,  quotes_type: str) -> List[str]:
    delimiter = quotes_type + separator + quotes_type

    # Remove new line and whitespaces at the end of line
    x = line.rstrip()

    column_names_list = [quotes_type + name + quotes_type for name in x.split(delimiter)]

    # Remove additional quotes_type at the end of last element in list
    return column_names_list


# Erases multiple whitespaces at start/end and removes quotes at both ends
def format_list(column_names_list: List[str], quotes_type: str) -> List[str]:
    new_list = []
    for name in column_names_list:
        new_name = name.strip()

        # remove quotes at the end of both sides
        while new_name.endswith(quotes_type):
            new_name = new_name[:-1]
        while new_name.startswith(quotes_type):
            new_name = new_name[1:]

        new_list.append(new_name)

    return new_list


def print_column_names_list(column_names_list: List[str]):
    print("List of column names:")
    for name in column_names_list:
        print(name, end=' ')
    print('\n')


class ColumnStats:
    def __init__(self, name: str):
        self.name = name
        self.wordsCount = 0
        self.sumOfCharacters = 0
        self.sumOfNotNullCharacters = 0
        self.longestRow = -1
        self.shortestRow = -1
        self.nulls = 0
        self.lengths = []

    def update(self, elem_length: int):
        self.wordsCount += 1
        self.sumOfCharacters += elem_length
        self.lengths.append(elem_length)

        if elem_length > 0:
            self.sumOfNotNullCharacters += elem_length
        else:
            self.nulls += 1

        self.longestRow = max(self.longestRow, elem_length)

        if self.shortestRow == -1:
            self.shortestRow = elem_length
        else:
            self.shortestRow = min(self.shortestRow, elem_length)

    # Prints statistics of analysed column i.e:
    #   -> mean
    #   -> median
    #   -> biggest_length
    #   -> shortest_length
    def print_statistics(self) -> None:
        if self.wordsCount == 0:
            print("No elements of this column")
        else:
            # Calculate average length
            mean = self.sumOfCharacters / self.wordsCount

            # Calculate median
            self.lengths.sort()
            median = self.lengths[self.wordsCount // 2]

            nice_pattern_chars = "===] Statistics for column {} [===".format(self.name).__len__()

            # Print results
            print("[===] Statistics for column {} [===]".format(self.name))
            print("Mean length: {}".format(mean))
            print("Median length: {}".format(median))
            print("Shortest element: {}".format(self.shortestRow))
            print("Longest element: {}".format(self.longestRow))
            print("[" + nice_pattern_chars * "=" + "]")


# Analyses row, returns number of elements and its sizes
def analise_row(row_list: List[str]) -> Tuple[int, List[int]]:
    elements_lengths = [elem.__len__() for elem in row_list]
    number_of_elements = elements_lengths.__len__()

    return number_of_elements, elements_lengths


def alert_wrong_number_of_values(line: str, number_of_elements: int,
                                 number_of_columns: int):
    print("[ERROR] Wrong number of values. Expected: {}, received: {}".format(
          number_of_columns, number_of_elements))
    print("Parsed line: " + line)


# Prints statistics of analysed csv i.e:
#   -> mean
#   -> median
#   -> biggest_length
#   -> shortest_length
def print_statistics(stats: List[ColumnStats]) -> None:
    for column in stats:
        column.print_statistics()


# Analyses csv file given in path
def analise_csv(path: str, separator: str = ',',  quotes_type: str = '"'):
    with open(path, "r", encoding='cp850') as csv_file:
        print("\n\nSuccessfully opened file {}\n".format(csv_file.name))

        # Reads first line of document which should be names of columns
        column_names_raw = csv_file.readline()

        # Check whether it's empty file
        if not column_names_raw:
            print("No columns detected")

        column_names_list = split_line(column_names_raw, separator, quotes_type)
        formatted_column_names_list = format_list(column_names_list, quotes_type)
        print_column_names_list(formatted_column_names_list)

        columns = [ColumnStats(col) for col in formatted_column_names_list]
        number_of_columns = columns.__len__()

        # Traverse all lines of csv_file
        for line in csv_file:
            row_list = split_line(line, separator, quotes_type)
            formatted_row_list = format_list(row_list, quotes_type)
            (number_of_elements, lengths) = analise_row(formatted_row_list)

            # Condition when there are not enough / too many elements in row
            if number_of_elements != number_of_columns:
                alert_wrong_number_of_values(line, number_of_elements,
                                             number_of_columns)
                print(row_list)
            else:
                for col, elem in zip(columns, lengths):
                    col.update(elem)

        print_statistics(columns)


# Checks whether value of element in one column infers the second one
def are_columns_dependant(path: str, column_a: str, column_b: str,
                          separator: str = ',',  quotes_type: str = '"'):
    with open(path, "r", encoding='cp850') as csv_file:
        print("\n\nSuccessfully opened file {}\n".format(csv_file.name))

        # Reads first line of document which should be names of columns
        column_names_raw = csv_file.readline()

        # Check whether it's empty file
        if not column_names_raw:
            print("No columns detected")

        column_names_list = split_line(column_names_raw, separator, quotes_type)
        formatted_column_names_list = format_list(column_names_list, quotes_type)
        print_column_names_list(formatted_column_names_list)

        # Check whether column_a and column_b exists
        index_a = -1
        index_b = -1
        col_number = -1
        for col in formatted_column_names_list:
            col_number += 1
            if col == column_a:
                index_a = col_number
            if col == column_b:
                index_b = col_number

        if index_a < 0 or index_b < 0:
            print("No column with that name")
            return False

        elements_dict = {}

        # Traverse all lines of csv_file
        for line in csv_file:
            row_list = split_line(line, separator, quotes_type)
            formatted_row_list = format_list(row_list, quotes_type)
            col_key = formatted_row_list[index_a]
            col_value = formatted_row_list[index_b]

            if col_key in elements_dict:
                x = elements_dict[col_key]

                if x != col_value:
                    print("Mismatch, previously defined value for key: {} is {} but now it is {}".format(col_key, x,
                                                                                                         col_value))
                    print(formatted_row_list)
                    return False
            else:
                elements_dict[col_key] = col_value

        print("Columns {} and {} are dependant".format(column_a, column_b))
        return True
