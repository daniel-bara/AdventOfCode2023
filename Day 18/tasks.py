from dataclasses import dataclass
import unittest

import regex


def main():
    with open("Day 18/input.txt") as file:
        lines = list(map(str.strip, file.readlines()))
    print(f"Task 1: {task1(lines)}")
    print(f"Task 2: {task2(lines)}")


class Instruction:
    def __init__(self, direction, length, coords) -> None:
        self.direction = direction
        self.length = int(length)
        self.coords = coords


def coords_add(coords, direction, length):
    if direction == "U":
        return (coords[0], coords[1] - length)
    if direction == "R":
        return (coords[0] + length, coords[1])
    if direction == "D":
        return (coords[0], coords[1] + length)
    if direction == "L":
        return (coords[0] - length, coords[1])


def task1(input):
    instructions = []
    coords = (0, 0)
    for line in input:
        m = regex.match(r"(?P<direction>U|R|D|L) (?P<length>\d+) \(#(?P<color>\w+)\)", line)
        instruction = Instruction(m.group("direction"), m.group("length"), coords)
        instructions.append(instruction)
        coords = coords_add(coords, instruction.direction, instruction.length)
    return calculate_area(instructions)


def calculate_area(instructions: list[Instruction]):
    area = 1
    for instr in instructions:
        area += instr.length/2
        area_calculation = {"R": (-1, 1), "D": (1, 0), "L": (1, 1), "U": (-1, 0)}
        values = area_calculation[instr.direction]
        area += instr.length * values[0] * instr.coords[values[1]] / 2
    return int(area)


def task2(input):
    instructions = []
    coords = (0, 0)
    for line in input:
        m = regex.match(r"(?P<direction>U|R|D|L) (?P<length>\d+) \(#(?P<color>\w+)\)", line)
        dir_int = int(m.group("color")[-1])
        dir_map = {0: "R", 1: "D", 2: "L", 3: "U"}
        instruction = Instruction(
            dir_map[dir_int],
            int(m.group("color")[:5], 16),
            coords)
        instructions.append(instruction)
        coords = coords_add(coords, instruction.direction, instruction.length)
    return calculate_area(instructions)


class Tests(unittest.TestCase):
    def setUp(self):
        with open("Day 18/input_test.txt") as file:
            self.lines_test = list(map(str.strip, file.readlines()))

    def test_square(self):
        self.assertEqual(task1([
            "R 4 (#70c710)",
            "D 4 (#0dc571)",
            'L 4 (#5713f0)',
            'U 4 (#d2c081)']), 25)

    def test(self):
        self.assertEqual(task1(self.lines_test), 62)

    def test2(self):
        self.assertEqual(task2(self.lines_test), 952408144115)


if __name__ == "__main__":
    unittest.main(exit=False)
    main()
