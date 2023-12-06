import unittest
import regex


def main():
    with open("Day 4/input.txt") as file:
        lines = list(map(str.strip, file.readlines()))
    print(f"Task 1: {task1(lines)}")
    print(f"Task 2: {task2(lines)}")


def task1(input):
    cards_points = []
    for line in input:
        matches = matches_on_line(line)
        points = 2**(matches-1) if matches > 0 else 0
        cards_points.append(points)
    return sum(cards_points)


def task2(input):
    match_map = dict(zip(range(len(input)), map(matches_on_line, input)))
    card_amounts = [1] * len(input)

    for card_index in range(len(card_amounts)):
        match_count = match_map[card_index]
        for i in range(match_count):
            card_amounts[card_index + i + 1] += card_amounts[card_index]

    return sum(card_amounts)


def matches_on_line(line):
    winning_numbers = list(map(int, regex.findall(
        r'\d+', line.split(":")[1].split("|")[0])))
    your_numbers = list(map(int, regex.findall(
        r'\d+', line.split(":")[1].split("|")[1])))

    return len(set(winning_numbers) & set(your_numbers))


class Tests(unittest.TestCase):
    def setUp(self):
        with open("Day 4/input_test.txt") as file:
            self.lines_test = list(map(str.strip, file.readlines()))

    def test(self):
        self.assertEqual(task1(self.lines_test), 13)

    def test2(self):
        self.assertEqual(task2(self.lines_test), 30)


if __name__ == "__main__":
    unittest.main(exit=False)
    main()
