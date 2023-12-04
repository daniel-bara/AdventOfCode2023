import unittest
import regex
from dataclasses import dataclass


def main():
    with open("Day 3/input.txt") as file:
        lines = list(map(str.strip, file.readlines()))
    print(f"Task 1: {task1(lines)}")
    print(f"Task 2: {task2(lines)}")


def task1(input):
    symbols = []
    for line in input:
        symbols.append(
            list(map(lambda match: match.start(), regex.finditer(r'[^\d\.]', line))))

    size_rows = len(input)
    size_cols = len(input[0])

    @dataclass
    class PartNumber:
        row: int
        column: int
        value: int
    part_numbers = []

    for row_index, line in enumerate(input):
        numbers = regex.finditer(r'\d+', line)
        for number_match in numbers:
            is_part_number = False
            for i, _ in enumerate(number_match.group(0)):
                if is_adjacent_to_any_symbol(row_index, i + number_match.start(), symbols, size_rows, size_cols):
                    is_part_number = True
            if is_part_number:
                part_numbers.append(PartNumber(
                    row_index, number_match.start(), int(number_match.group(0))))
    return sum(map(lambda pn: pn.value, part_numbers))


def task2(input):
    symbols = []
    for line in input:
        symbols.append(
            list(map(lambda match: match.start(), regex.finditer(r'[^\d\.]', line))))

    size_rows = len(input)
    size_cols = len(input[0])

    @dataclass
    class PartNumber:
        row: int
        column: int
        value: int
        adjacent_symbols: list

    part_numbers = []

    for row_index, line in enumerate(input):
        numbers = regex.finditer(r'\d+', line)
        for number_match in numbers:
            is_part_number = False
            adjacent_symbols = []
            for i, _ in enumerate(number_match.group(0)):
                if symbol_pos := is_adjacent_to_any_symbol(row_index, i + number_match.start(), symbols, size_rows, size_cols):
                    is_part_number = True
                    adjacent_symbols.append(symbol_pos)
            if is_part_number:
                part_numbers.append(PartNumber(
                    row_index, number_match.start(), int(number_match.group(0)), adjacent_symbols))
                
    gear_symbols = []
    for row_index, col_indices in enumerate(symbols):
        for col_index in col_indices:
            adjacent_part_numbers = list(filter(lambda part_number: (row_index, col_index) in part_number.adjacent_symbols, part_numbers))
            if len(adjacent_part_numbers) == 2:
                gear_symbols.append(adjacent_part_numbers[0].value * adjacent_part_numbers[1].value)
                
    return sum(gear_symbols)


def is_adjacent_to_any_symbol(row, column, symbol_locations, size_rows, size_cols):
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                lookup_row = row + y
                lookup_col = column + x
                if not 0 <= lookup_row < size_rows:
                    continue
                if not 0 <= lookup_col < size_cols:
                    continue
                if lookup_col in symbol_locations[lookup_row]:
                    return (lookup_row, lookup_col)
        return False


class Tests(unittest.TestCase):
    def setUp(self):
        with open("Day 3/input_test.txt") as file:
            self.lines_test = list(map(str.strip, file.readlines()))
        with open("Day 3/input_test.txt") as file:
            self.lines_test2 = list(map(str.strip, file.readlines()))

    def test(self):
        self.assertEqual(task1(self.lines_test), 4361)

    def test2(self):
        self.assertEqual(task2(self.lines_test2), 467835)


if __name__ == "__main__":
    unittest.main(exit=False)
    main()
