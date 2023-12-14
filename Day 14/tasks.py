import copy
import time
import unittest


def main():
    with open("Day 14/input.txt") as file:
        lines = list(map(str.strip, file.readlines()))
    print(f"Task 1: {task1(lines)}")
    print(f"Task 2: {task2(lines)}")


class Terrain:
    def __init__(self, lines):
        self.matrix = [list(line) for line in lines]
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])

    def try_roll_north_once(self):
        rolled = False
        for row_i, line in enumerate(self.matrix):
            for col_i, char in enumerate(line):
                if char == "O" and 0 < row_i and self.matrix[row_i-1][col_i] == ".":
                    self.matrix[row_i-1][col_i] = "O"
                    self.matrix[row_i][col_i] = "."
                    rolled = True
        return rolled

    def try_roll_west_once(self):
        rolled = False
        for row_i, line in enumerate(self.matrix):
            for col_i, char in enumerate(line):
                if char == "O" and 0 < col_i and self.matrix[row_i][col_i-1] == ".":
                    self.matrix[row_i][col_i-1] = "O"
                    self.matrix[row_i][col_i] = "."
                    rolled = True
        return rolled

    def try_roll_south_once(self):
        rolled = False
        for row_i, line in enumerate(self.matrix):
            for col_i, char in enumerate(line):
                if char == "O" and row_i < self.rows-1 and self.matrix[row_i+1][col_i] == ".":
                    self.matrix[row_i+1][col_i] = "O"
                    self.matrix[row_i][col_i] = "."
                    rolled = True
        return rolled

    def try_roll_east_once(self):
        rolled = False
        for row_i, line in enumerate(self.matrix):
            for col_i, char in enumerate(line):
                if char == "O" and col_i < self.cols-1 and self.matrix[row_i][col_i+1] == ".":
                    self.matrix[row_i][col_i+1] = "O"
                    self.matrix[row_i][col_i] = "."
                    rolled = True
        return rolled

    def roll_rocks_north(self):
        while self.try_roll_north_once():
            pass

    def roll_rocks_west(self):
        while self.try_roll_west_once():
            pass

    def roll_rocks_south(self):
        while self.try_roll_south_once():
            pass

    def roll_rocks_east(self):
        while self.try_roll_east_once():
            pass

    def cycle(self, repetitions=1):
        last_cycle_results = [hash(self)]
        skipped = False
        while repetitions > 0:
            self.roll_rocks_north()
            self.roll_rocks_west()
            self.roll_rocks_south()
            self.roll_rocks_east()
            if not skipped:
                for i in range(len(last_cycle_results)):
                    i_back = -i-1
                    if hash(self) == last_cycle_results[i_back]:
                        print(f"loop found, skipping to { repetitions % (i+1)}")
                        repetitions = repetitions % (i+1)
                        skipped = True
            last_cycle_results.append(hash(self))
            repetitions -= 1

    def calculate_weight(self):
        return sum(map(self.calculate_col_weight, range(self.cols)))

    def calculate_col_weight(self, col_i):
        weight = 0
        for row_i in range(self.rows):
            if self.matrix[row_i][col_i] == "O":
                weight += self.rows - row_i
        return weight

    def __str__(self) -> str:
        return "\n".join(map(lambda line: "".join(line), self.matrix))
    
    def __hash__(self):
        return hash(tuple(map(lambda line: tuple(line), self.matrix)))


def task1(input):
    terrain = Terrain(input)
    terrain.roll_rocks_north()
    return terrain.calculate_weight()


def task2(input):
    sw = time.time()
    terrain = Terrain(input)
    terrain.cycle(1000000000)
    print(f"Time elapsed: {time.time()-sw}")
    return terrain.calculate_weight()


class Tests(unittest.TestCase):
    def setUp(self):
        with open("Day 14/input_test.txt") as file:
            self.lines_test = list(map(str.strip, file.readlines()))
        with open("Day 14/test_cycle_1.txt") as file:
            self.test_cycle_1 = list(map(str.strip, file.readlines()))

    def test(self):
        self.assertEqual(task1(self.lines_test), 136)

    def test_one_cycle(self):
        terrain = Terrain(self.lines_test)
        terrain.cycle(1)
        self.assertEqual(str(terrain), "\n".join(self.test_cycle_1))

    def test2(self):
        terrain = Terrain(self.lines_test)
        terrain.cycle(1000000000)
        self.assertEqual(terrain.calculate_weight(), 64)


if __name__ == "__main__":
    unittest.main(exit=False)
    main()
