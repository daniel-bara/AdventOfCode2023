import unittest


def main():
    with open("Day 0/input.txt") as file:
        lines = list(map(str.strip, file.readlines()))
    print(f"Task 1: {task1(lines)}")
    print(f"Task 2: {task2(lines)}")


def task1(input):
    return -1


def task2(input):
    return -1


class Tests(unittest.TestCase):
    def setUp(self):
        with open("Day 0/input_test.txt") as file:
            self.lines_test = list(map(str.strip, file.readlines()))
        with open("Day 0/input_test2.txt") as file:
            self.lines_test2 = list(map(str.strip, file.readlines()))

    def test(self):
        self.assertEqual(task1(self.lines_test), 0)

    def test2(self):
        self.assertEqual(task2(self.lines_test2), 0)
    
    def test3(self):
        self.assertEqual(task2(["asdf"]), 0)


if __name__ == "__main__":
    unittest.main(exit=False)
    main()
