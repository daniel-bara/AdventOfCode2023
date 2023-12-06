import math
import unittest
import regex
import itertools


def main():
    with open("Day 2/input.txt") as file:
        lines = list(map(str.strip, file.readlines()))
    print(f'Task 1: {task1(lines, {"red": 12, "green": 13, "blue": 14})}')
    print(f"Task 2: {task2(lines)}")


class Draw:
    def __init__(self, regex_match):
        self.amount = int(regex_match[0])
        self.color = regex_match[1]

    def find_all_in_line(line):
        return list(map(lambda x: Draw(x), regex.findall(r'(\d+) (red|green|blue)', line)))


def task1(lines, color_amounts):
    line_invalidation = {}
    for line in lines:
        game_index = int(regex.match(r'Game (\d+)', line).group(1))
        line_invalidation[game_index] = "unknown"
        draws = Draw.find_all_in_line(line)
        for draw in draws:
            if draw.amount > color_amounts[draw.color]:
                line_invalidation[game_index] = "invalid"
    return sum(map(lambda pair: pair[0], filter(lambda pair: pair[1] != "invalid", line_invalidation.items())))


def task2(lines):
    line_powers = []
    for line in lines:
        color_minimums = {}
        draws = Draw.find_all_in_line(line)
        for draw in draws:
            if draw.amount > color_minimums.get(draw.color, 0):
                color_minimums[draw.color] = draw.amount
        line_powers.append(math.prod(color_minimums.values()))
    return sum(line_powers)


class Tests(unittest.TestCase):
    def setUp(self):
        with open("Day 2/input_test.txt") as file:
            self.lines_test = list(map(str.strip, file.readlines()))

    def test(self):
        self.assertEqual(
            task1(self.lines_test, {"red": 12, "green": 13, "blue": 14}), 8)

    def test2(self):
        self.assertEqual(task2(self.lines_test), 2286)

    def test3(self):
        pass


if __name__ == "__main__":
    unittest.main(exit=False)
    main()
