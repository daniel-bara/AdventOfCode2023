import unittest
import regex


def main():
    with open("Day 1/input.txt") as file:
        lines = list(map(str.strip, file.readlines()))
    print(task1(lines))
    print(task2(lines))


def task1(input):
    def first_and_last(input_list):
        return (input_list[0], input_list[-1])
    return sum(map(
        lambda line: int(''.join(first_and_last(regex.findall(r'\d', line)))),
        input))


def task2(input):
    def first_and_last(input_list):
        return (input_list[0], input_list[-1])

    def substitute_written_digits(input_string):
        lookup = {"one": 1, "two": 2, "three": 3, "four": 4,
                  "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}
        for key, value in lookup.items():
            input_string = regex.sub(key, str(value), input_string)
        return input_string

    return sum(map(
        lambda line: int(substitute_written_digits(''.join(first_and_last(
            regex.findall(r'(\d|one|two|three|four|five|six|seven|eight|nine)', line, overlapped=True))))),
        input))


class Tests(unittest.TestCase):
    def setUp(self):
        with open("Day 1/input_test.txt") as file:
            self.lines_test = list(map(str.strip, file.readlines()))
        with open("Day 1/input_test2.txt") as file:
            self.lines_test2 = list(map(str.strip, file.readlines()))

    def test(self):
        self.assertEqual(task1(self.lines_test), 142)

    def test2(self):
        self.assertEqual(task2(self.lines_test2), 281)
    
    def test3(self):
        self.assertEqual(task2(["2xxxxnnnvxvheightwobm"]), 22)


if __name__ == "__main__":
    unittest.main(exit=False)
    main()
