import itertools
import unittest


def main():
    with open("Day 11/input.txt") as file:
        lines = list(map(str.strip, file.readlines()))
    print(f"Task 1: {task1(lines)}")
    print(f"Task 2: {task2(lines)}")


def number_is_between(x, a, b):
    return (x > a) != (x > b)


class Galaxy:
    def __init__(self, lines) -> None:
        self.matrix = lines
        self.duplicated_rows = []
        self.duplicated_cols = []
        self.galaxies_coords = None

    def expand(self):
        rows_with_galaxies = set(
            map(lambda coords: coords[1], self.get_galaxies_coords()))
        self.duplicated_rows = list(
            filter(lambda row: row not in rows_with_galaxies, range(len(self.matrix))))

        cols_with_galaxies = set(
            map(lambda coords: coords[0], self.get_galaxies_coords()))
        self.duplicated_cols = list(
            filter(lambda col: col not in cols_with_galaxies, range(len(self.matrix[0]))))

    def sum_distances(self, expansion_multiplier=1):
        return sum(map(lambda pair: self.distance_between(pair[0], pair[1], expansion_multiplier), self.get_pairs()))

    def distance_between(self, coords1, coords2, expansion_multiplier):
        dst_x = abs(coords2[0] - coords1[0]) + \
            sum([1 for x in self.duplicated_cols
                if number_is_between(x, coords2[0], coords1[0])]) * expansion_multiplier
        dst_y = abs(coords2[1] - coords1[1]) + \
            sum([1 for x in self.duplicated_rows
                if number_is_between(x, coords2[1], coords1[1])]) * expansion_multiplier
        return dst_x + dst_y

    def get_galaxies_coords(self):
        if self.galaxies_coords is None:
            self.galaxies_coords = []
            for index_y, line in enumerate(self.matrix):
                for index_x, char in enumerate(line):
                    if char == "#":
                        self.galaxies_coords.append((index_x, index_y))
        return self.galaxies_coords

    def get_pairs(self):
        return itertools.combinations(self.get_galaxies_coords(), 2)

    def __str__(self) -> str:
        output = ""
        for index_y, line in enumerate(self.matrix):
            printed_line = ""
            for index_x, char in enumerate(line):
                if printed_line in self.duplicated_cols:
                    line += char * 2
                else:
                    printed_line += char
            if index_y in self.duplicated_rows:
                output += ("\n" + printed_line) * 2
            else:
                output += "\n" + printed_line
        return output


def task1(input):
    galaxy = Galaxy(input)
    galaxy.expand()
    return galaxy.sum_distances()


def task2(input, expansion_multiplier=999999):
    galaxy = Galaxy(input)
    galaxy.expand()
    return galaxy.sum_distances(expansion_multiplier)


class Tests(unittest.TestCase):
    def setUp(self):
        with open("Day 11/input_test.txt") as file:
            self.lines_test = list(map(str.strip, file.readlines()))
        with open("Day 11/input_test2.txt") as file:
            self.lines_test2 = list(map(str.strip, file.readlines()))

    def test_number_is_between(self):
        self.assertEqual(number_is_between(15, 14, 16), True)
        self.assertEqual(number_is_between(15, 16, 14), True)
        self.assertEqual(number_is_between(13, 14, 16), False)

    def test(self):
        self.assertEqual(task1(self.lines_test), 374)

    def test2(self):
        self.assertEqual(task2(self.lines_test, expansion_multiplier=9), 1030)
        self.assertEqual(task2(self.lines_test, expansion_multiplier=99), 8410)


if __name__ == "__main__":
    unittest.main(exit=False)
    main()
