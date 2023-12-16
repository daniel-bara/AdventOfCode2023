from dataclasses import dataclass
import unittest
import regex


def main():
    with open("Day 15/input.txt") as file:
        lines = list(map(str.strip, file.readlines()))
    print(f"Task 1: {task1(lines)}")
    print(f"Task 2: {task2(lines)}")


def custom_hash(s: str):
    val = 0
    for c in s:
        val += ord(c)
        val *= 17
        val %= 256
    return val


def task1(input):
    return sum(map(custom_hash, input[0].split(",")))


@dataclass
class Lens:
    label: str
    number: int


def task2(input):
    boxes = [[] for _ in range(256)]
    for instruction in input[0].split(","):
        match = regex.match(r'(?P<label>\w+)(?P<operator>-|=)(?P<number>\d?)', instruction)
        box = boxes[custom_hash(match.group("label"))]

        if match.group("operator") == "=":
            lens = Lens(match.group("label"), match.group("number"))
            if any(filter(lambda lens: lens.label == match.group("label"), box)):
                lens_to_modify = next(filter(lambda lens: lens.label == match.group("label"), box))
                lens_to_modify.number = lens.number
            else:
                box.append(lens)
        elif any(lenses_to_remove := list(filter(lambda lens: lens.label == match.group("label"), box))):
            box.remove(lenses_to_remove[0])

    focusing_power = 0
    for box_index, box in enumerate(boxes):
        for lens_index, lens in enumerate(box):
            focusing_power += (box_index + 1) * (lens_index + 1) * int(lens.number)
    return focusing_power


class Tests(unittest.TestCase):
    def setUp(self):
        with open("Day 15/input_test.txt") as file:
            self.lines_test = list(map(str.strip, file.readlines()))

    def test(self):
        self.assertEqual(task1(self.lines_test), 1320)

    def test2(self):
        self.assertEqual(custom_hash("rn"), 0)
        self.assertEqual(task2(self.lines_test), 145)


if __name__ == "__main__":
    unittest.main(exit=False)
    main()
