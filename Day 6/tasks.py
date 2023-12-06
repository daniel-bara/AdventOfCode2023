import unittest
import regex
import math


def main():
    with open("Day 6/input.txt") as file:
        lines = list(map(str.strip, file.readlines()))
    print(f"Task 1: {task1(lines)}")
    print(f"Task 2: {task2(lines)}")


def task1(input):
    times = list(map(int, regex.findall(r'\d+', input[0])))
    distances = list(map(int, regex.findall(r'\d+', input[1])))
    win_counts = []
    for race_index in range(len(times)):
        win_count = 0
        for i in range(times[race_index]):
            if i*(times[race_index]-i) > distances[race_index]:
                win_count += 1
        win_counts.append(win_count)
    return math.prod(win_counts)


def task2(input):
    time = int("".join(regex.findall(r'\d+', input[0])))
    distance = int("".join(regex.findall(r'\d+', input[1])))
    # quadratic equation:
    # -x^2 + time * x - distance = 0

    return int((time**2 - 4*distance)**0.5)


class Tests(unittest.TestCase):
    def setUp(self):
        with open("Day 6/input_test.txt") as file:
            self.lines_test = list(map(str.strip, file.readlines()))

    def test(self):
        self.assertEqual(task1(self.lines_test), 288)

    def test2(self):
        self.assertEqual(task2(self.lines_test), 71503)


if __name__ == "__main__":
    unittest.main(exit=False)
    main()
